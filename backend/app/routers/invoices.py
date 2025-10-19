from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice import Invoice, InvoiceItem
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from datetime import datetime

from fastapi.responses import FileResponse
from jinja2 import Template
import tempfile
from weasyprint import HTML

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

# --------------------------
#  Fatura OLUŞTURMA
# --------------------------
@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == invoice_data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    subtotal = 0
    vat_total = 0
    discount_total = 0
    items = []

    # Ürün satırlarını hesapla
    for item_data in invoice_data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item_data.product_id} not found")

        unit_price = product.price
        discount_amount = unit_price * item_data.quantity * (item_data.discount_rate / 100)
        vat_amount = (unit_price * item_data.quantity - discount_amount) * (product.vat / 100)
        line_total = (unit_price * item_data.quantity - discount_amount) + vat_amount

        subtotal += unit_price * item_data.quantity
        vat_total += vat_amount
        discount_total += discount_amount

        item = InvoiceItem(
            product_id=product.id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            discount_rate=item_data.discount_rate,
            vat_rate=product.vat,
            line_total=line_total
        )
        items.append(item)

    grand_total = subtotal + vat_total - discount_total

    invoice = Invoice(
        date=datetime.now(),
        customer_id=customer.id,
        subtotal=subtotal,
        vat_total=vat_total,
        discount_total=discount_total,
        grand_total=grand_total,
        items=items
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

# --------------------------
#  Fatura PDF OLUŞTURMA
# --------------------------
@router.get("/{invoice_id}/pdf", response_class=FileResponse)
def generate_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    customer = invoice.customer
    items = invoice.items

    html_template = Template("""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: DejaVu Sans, sans-serif; margin: 40px; color: #222; }
            h1 { text-align: center; color: #444; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #888; padding: 8px; text-align: right; }
            th { background-color: #f2f2f2; }
            .left { text-align: left; }
            .summary td { font-weight: bold; }
            footer { text-align: center; margin-top: 40px; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <h1>FATURA</h1>
        <p><strong>Tarih:</strong> {{ invoice.date.strftime('%d.%m.%Y %H:%M') }}</p>
        <p><strong>Müşteri:</strong> {{ customer.name }}</p>
        <p><strong>Vergi No:</strong> {{ customer.tax_number }}</p>
        <p><strong>Adres:</strong> {{ customer.address }}</p>

        <table>
            <tr>
                <th class="left">Ürün Adı</th>
                <th>Miktar</th>
                <th>Birim Fiyat (₺)</th>
                <th>İskonto (%)</th>
                <th>KDV (%)</th>
                <th>Satır Toplamı (₺)</th>
            </tr>
            {% for item in items %}
            <tr>
                <td class="left">{{ item.product.name }}</td>
                <td>{{ "%.2f"|format(item.quantity) }}</td>
                <td>{{ "%.2f"|format(item.unit_price) }}</td>
                <td>{{ "%.1f"|format(item.discount_rate) }}</td>
                <td>{{ "%.1f"|format(item.vat_rate) }}</td>
                <td>{{ "%.2f"|format(item.line_total) }}</td>
            </tr>
            {% endfor %}
        </table>

        <table class="summary" style="margin-top: 25px;">
            <tr><td class="left">Ara Toplam</td><td>{{ "%.2f"|format(invoice.subtotal) }} ₺</td></tr>
            <tr><td class="left">KDV Toplam</td><td>{{ "%.2f"|format(invoice.vat_total) }} ₺</td></tr>
            <tr><td class="left">İskonto Toplam</td><td>{{ "%.2f"|format(invoice.discount_total) }} ₺</td></tr>
            <tr><td class="left">Genel Toplam</td><td>{{ "%.2f"|format(invoice.grand_total) }} ₺</td></tr>
        </table>

        <footer>
            <p>Bu belge MFP (Market Fatura Platformu) tarafından otomatik oluşturulmuştur.</p>
        </footer>
    </body>
    </html>
    """)

    html_content = html_template.render(invoice=invoice, customer=customer, items=items)

    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html_content).write_pdf(pdf_file.name)

    return FileResponse(pdf_file.name, filename=f"Fatura_{invoice.id}.pdf", media_type="application/pdf")
