# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from weasyprint import HTML, CSS
import os
from jinja2 import Template
from fastapi.responses import FileResponse
from app.database import get_db
from app.models.invoice import Invoice, InvoiceItem
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.invoice import InvoiceCreate
from app.models.user import User, RoleEnum
from app.core.security import get_current_user, rep_required

router = APIRouter(prefix="/invoices", tags=["Invoices"])


# --------------------- Yardımcı Fonksiyonlar ---------------------

def tl_format(x):
    try:
        return f"₺{float(x):,.2f}".replace(",", ".").replace(".", ",", 1)
    except Exception:
        return "₺0,00"


def get_logo_path():
    """Logo yolunu sistemden otomatik olarak çeker"""
    static_path = os.path.join("app", "static", "ertan.png")
    if os.path.exists(static_path):
        return f"file:///{os.path.abspath(static_path).replace(os.sep, '/')}"
    return None


# --------------------- Fatura Oluşturma ---------------------

@router.post("/create")
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Yeni fatura oluşturur ve PDF olarak döner"""
    if current_user.role not in [RoleEnum.admin, RoleEnum.representative]:
        raise HTTPException(status_code=403, detail="Fatura oluşturma yetkiniz yok.")

    customer = db.query(Customer).filter(Customer.id == invoice_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı.")

    # Fatura numarası otomatik üretim
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    if last_invoice:
        next_id = last_invoice.id + 1
    else:
        next_id = 1
    fatura_no = f"FAT-{datetime.now().year}-{next_id:05d}"

    # Hesap değişkenleri
    subtotal = 0.0
    total_discount = 0.0
    total_vat = 0.0
    items = []

    for item_data in invoice_data.items[:25]:  # maksimum 25 satır
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            continue

        # Ürün fiyatı alımı (unit_price zorunlu)
        unit_price = float(product.unit_price or 0)
        quantity = float(item_data.quantity or 0)
        discount_rate = float(item_data.discount_rate or 0)
        try:
            vat_rate = float(product.vat_rate.value)
        except Exception:
            try:
                vat_rate = float(product.vat_rate)
            except Exception:
                vat_rate = 0.0

        raw_total = unit_price * quantity
        discount_amount = raw_total * discount_rate / 100
        vat_amount = (raw_total - discount_amount) * vat_rate / 100

        subtotal += raw_total
        total_discount += discount_amount
        total_vat += vat_amount

        item = InvoiceItem(
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            discount_rate=discount_rate,
            vat_rate=vat_rate,
            line_total=raw_total - discount_amount + vat_amount
        )
        items.append(item)

    grand_total = subtotal - total_discount + total_vat

    # Fatura nesnesi
    invoice = Invoice(
        date=datetime.now(),
        customer_id=customer.id,
        fatura_no=fatura_no,
        subtotal=subtotal,
        vat_total=total_vat,
        discount_total=total_discount,
        grand_total=grand_total,
        items=items
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    pdf_path = generate_invoice_pdf(invoice, customer, items)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"Fatura_{invoice.id}.pdf")


# --------------------- Fatura PDF Alma ---------------------

@router.get("/{invoice_id}/pdf")
def get_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Var olan faturayı PDF olarak indirir"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Fatura bulunamadı.")

    # Eğer kullanıcı müşteri ise sadece kendi faturasını görebilmeli
    if current_user.role == RoleEnum.customer and current_user.customer_id != invoice.customer_id:
        raise HTTPException(status_code=403, detail="Bu faturaya erişim yetkiniz yok.")

    customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
    items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()

    pdf_path = generate_invoice_pdf(invoice, customer, items)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"Fatura_{invoice_id}.pdf")


# --------------------- PDF Oluşturucu ---------------------

def generate_invoice_pdf(invoice, customer, items):
    """HTML + CSS tabanlı PDF çıktısı üretir"""
    logo_path = get_logo_path()

    html_template = Template("""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: DejaVu Sans, sans-serif;
                font-size: 11px;
                margin: 20px 25px;
                color: #222;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
            }
            .header img { width: 120px; }
            .invoice-info {
                text-align: right;
                border: 1px solid #999;
                padding: 6px 10px;
                border-radius: 4px;
                background: #f9f9f9;
                font-size: 10px;
            }
            .customer {
                margin-top: 5px;
                line-height: 1.4;
                font-size: 10.5px;
            }
            h1 {
                text-align: center;
                color: #7a1c1c;
                margin: 8px 0;
                font-size: 15px;
                text-transform: uppercase;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 8px;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 5px;
                text-align: center;
                font-size: 10.5px;
                word-wrap: break-word;
            }
            th {
                background: #7a1c1c;
                color: white;
            }
            tr:nth-child(even) { background: #f9f9f9; }

            th:nth-child(1), td:nth-child(1) { width: 10%; }
            th:nth-child(2), td:nth-child(2) { width: 43%; text-align: left; padding-left: 6px; }
            th:nth-child(3), td:nth-child(3) { width: 8%; }
            th:nth-child(4), td:nth-child(4) { width: 10%; }
            th:nth-child(5), td:nth-child(5) { width: 8%; }
            th:nth-child(6), td:nth-child(6) { width: 7%; }
            th:nth-child(7), td:nth-child(7) { width: 14%; }

            .totals {
                margin-top: 18px;
                width: 38%;
                float: right;
                font-size: 11px;
            }
            .totals td {
                border: none;
                padding: 3px 0;
                text-align: right;
            }
            .sign {
                width: 100%;
                margin-top: 100px;
                text-align: center;
                position: absolute;
                bottom: 75px;
            }
            .sign td {
                width: 50%;
                padding-top: 25px;
                font-size: 11px;
            }
            .footer {
                position: absolute;
                bottom: 15px;
                width: 100%;
                text-align: center;
                font-size: 9px;
                color: gray;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                {% if logo_path %}
                <img src="{{ logo_path }}" alt="Logo"><br>
                {% endif %}
                <div class="customer">
                    <b>{{ customer.name }}</b><br>
                    Vergi No: {{ customer.tax_number or '-' }}<br>
                    {{ customer.address or '' }}
                </div>
            </div>
            <div class="invoice-info">
                <b>Fatura No:</b> {{ invoice.fatura_no }}<br>
                <b>Tarih:</b> {{ invoice.date.strftime('%d.%m.%Y %H:%M') }}
            </div>
        </div>

        <h1>Satış Faturası</h1>

        <table>
            <tr>
                <th>Barkod</th>
                <th>Ürün Adı</th>
                <th>Miktar</th>
                <th>Birim Fiyat</th>
                <th>İskonto (%)</th>
                <th>KDV (%)</th>
                <th>Tutar</th>
            </tr>
            {% for item in items %}
            <tr>
                <td>{{ item.product.barcode or '-' }}</td>
                <td>{{ item.product.name }}</td>
                <td>{{ item.quantity }}</td>
                <td>{{ tl_format(item.unit_price) }}</td>
                <td>{{ item.discount_rate or 0 }}</td>
                <td>{{ item.vat_rate or 0 }}</td>
                <td>{{ tl_format(item.line_total) }}</td>
            </tr>
            {% endfor %}
        </table>

        <table class="totals">
            <tr><td>Ara Toplam:</td><td>{{ tl_format(invoice.subtotal) }}</td></tr>
            <tr><td>İskonto:</td><td>-{{ tl_format(invoice.discount_total) }}</td></tr>
            <tr><td>KDV:</td><td>{{ tl_format(invoice.vat_total) }}</td></tr>
            <tr><td><b>Genel Toplam:</b></td><td><b>{{ tl_format(invoice.grand_total) }}</b></td></tr>
        </table>

        <table class="sign">
            <tr>
                <td>_________________________<br><b>Teslim Eden</b></td>
                <td>_________________________<br><b>Teslim Alan</b></td>
            </tr>
        </table>

        <div class="footer">
            Bu belge MFP tarafından otomatik oluşturulmuştur.
        </div>
    </body>
    </html>
    """)

    rendered_html = html_template.render(
        logo_path=logo_path,
        invoice=invoice,
        customer=customer,
        items=items,
        tl_format=tl_format,
    )

    output_path = os.path.join("app", f"Fatura_{invoice.id}.pdf")
    HTML(string=rendered_html).write_pdf(
        output_path,
        stylesheets=[CSS(string="body { font-family: DejaVu Sans; }")]
    )
    return output_path
