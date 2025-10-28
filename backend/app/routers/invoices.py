# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from weasyprint import HTML, CSS
import os
from jinja2 import Template
from fastapi.responses import FileResponse, JSONResponse
from app.database import get_db
from app.models.invoice import Invoice, InvoiceItem # Bu modellerin DB'de tanımlı olması gerekir
from app.models.customer import Customer # Bu modelin DB'de tanımlı olması gerekir
from app.models.product import Product # Bu modelin DB'de tanımlı olması gerekir
from app.schemas.invoice import InvoiceCreate
from app.models.user import RoleEnum # RoleEnum'u doğrudan modelden çekiyoruz
from app.core.security import get_current_user, rep_required

# Fatura router'ınızı diğer router'lar gibi /api/v1/invoices altına dahil etmeliyiz.
router = APIRouter(prefix="/invoices", tags=["Invoices"])

# --------------------- Yardımcı Fonksiyonlar ---------------------

def tl_format(x):
    """Para birimi formatlama fonksiyonu."""
    try:
        # Türkiye'de yaygın kullanılan format (binlik ayraç nokta, ondalık ayraç virgül)
        return f"₺{float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "₺0,00"

def get_logo_path():
    """Logo yolunu sistemden otomatik olarak çeker"""
    # Statik dosyaların yolunu doğru ayarlıyoruz.
    static_path = os.path.join(os.getcwd(), "app", "static", "ertan.png")
    if os.path.exists(static_path):
        return f"file:///{os.path.abspath(static_path).replace(os.sep, '/')}"
    return None

# --------------------- Fatura Oluşturma ---------------------

@router.post("/create", dependencies=[Depends(rep_required)])
def create_invoice_and_pdf(
    invoice_data: InvoiceCreate, 
    db: Session = Depends(get_db), 
    # Current user artık sadece bir dict döndürüyor, role kontrolü rep_required içinde.
    current_user: dict = Depends(get_current_user) 
):
    """Yeni fatura oluşturur ve PDF olarak döner (Admin/Temsilci yetkisi gerektirir)."""
    
    # Simülasyon: Veritabanı sorguları yerine dummy veriler kullanıyoruz
    
    # 1. Müşteri Kontrolü (Simülasyon)
    if invoice_data.customer_id != 101: # 101 id'li müşteriyi simüle ediyoruz
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı. ID: 101 bekleniyor.")

    # 2. Fatura Numarası (Simülasyon)
    fatura_no = f"FAT-{datetime.now().year}-00001" 

    subtotal = total_discount = total_vat = 0.0
    items_pdf_data = [] # PDF çıktısı için kullanılacak kalemler

    # Gerçek uygulamada DB'den çekilmesi gereken Product bilgileri
    PRODUCT_SIMULATION = {"id": 1, "barcode": "12345", "unit_price": 500.0, "vat_rate": 20.0, "name": "Yazılım Geliştirme Hizmeti"}

    for idx, item_data in enumerate(invoice_data.items):
        product_info = PRODUCT_SIMULATION.copy() # Ürün bilgilerini simüle ediyoruz
        
        # Sizin kodunuzdaki karmaşık hesaplama mantığını sadeleştiriyoruz
        unit_price = product_info['unit_price']
        quantity = item_data.quantity
        discount_rate = item_data.discount_rate or 0 # DiscountRate şemada yoktu, varsayılan 0
        vat_rate = product_info['vat_rate'] / 100 # %20 -> 0.20

        raw_total = unit_price * quantity
        discount_amount = raw_total * discount_rate / 100
        vat_amount = (raw_total - discount_amount) * vat_rate
        line_total = raw_total - discount_amount + vat_amount

        subtotal += raw_total
        total_discount += discount_amount
        total_vat += vat_amount

        # PDF çıktısı için gereken veriler
        items_pdf_data.append({
            "product": {"barcode": product_info['barcode'], "name": product_info['name']},
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_rate": discount_rate,
            "vat_rate": product_info['vat_rate'], # %20 olarak gösterim
            "line_total": line_total,
        })

    grand_total = subtotal - total_discount + total_vat

    # Simüle edilmiş fatura objesi (PDF için gerekli)
    simulated_invoice = {
        "id": 1,
        "date": datetime.now(),
        "fatura_no": fatura_no,
        "subtotal": subtotal,
        "vat_total": total_vat,
        "discount_total": total_discount,
        "grand_total": grand_total,
    }
    
    # Simüle edilmiş Müşteri objesi (PDF için gerekli)
    simulated_customer = {
        "name": "Örnek Ticaret Ltd. Şti.",
        "tax_number": "9999999999",
        "address": "İstanbul, Türkiye",
        "id": 101
    }

    # Gerçek DB işlemi yerine PDF oluşturucu çağrılır
    pdf_path = generate_invoice_pdf(simulated_invoice, simulated_customer, items_pdf_data)
    
    # PDF'i FileResponse olarak döndür
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"Fatura_{simulated_invoice['fatura_no']}.pdf")


# --------------------- PDF Oluşturucu ---------------------

def generate_invoice_pdf(invoice, customer, items):
    """HTML + CSS tabanlı PDF çıktısı üretir"""
    
    # PDF oluşturma mantığı büyük ölçüde korundu
    logo_path = get_logo_path()

    html_template = Template("""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page { size: A4; margin: 20px 25px; }
            body {
                font-family: DejaVu Sans, sans-serif;
                font-size: 11px;
                color: #222;
                position: relative;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
                width: 100%;
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
                position: absolute;
                bottom: 75px;
                width: 95%;
                text-align: center;
            }
            .sign td {
                width: 50%;
                padding-top: 25px;
                font-size: 11px;
                border: none;
            }
            .footer {
                position: absolute;
                bottom: 15px;
                width: 95%;
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

    # PDF oluşturma geçici olarak /tmp (veya geçerli dizinde) yapılmalıdır.
    output_path = os.path.join(os.getcwd(), f"Fatura_Temp_{invoice['id']}.pdf")
    
    # Weasyprint, Türkçe karakterler için 'DejaVu Sans' gibi bir fonta ihtiyaç duyar.
    HTML(string=rendered_html).write_pdf(
        output_path,
        stylesheets=[CSS(string="@font-face { font-family: 'DejaVu Sans'; src: url('file:///usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'); }")]
    )
    return output_path