import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000/api")

class APIError(Exception):
    """Basit hata sınıfı."""
    pass


class APIClient:
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.token: Optional[str] = None

    # --- Auth ---
    def login(self, username: str, password: str) -> str:
        url = f"{self.base_url}/auth/login"
    # FastAPI Form beklediği için form-data gönderiyoruz:
        data = {"username": username, "password": password}
        resp = self.session.post(url, data=data, timeout=30)
        if resp.status_code >= 400:
            raise APIError(f"Giriş başarısız: {resp.status_code} {resp.text}")
        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise APIError("Token alınamadı.")
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    # --- Customers ---
    def get_customers(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/customers"
        r = self.session.get(url, timeout=30)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    def create_customer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/customers"
        r = self.session.post(url, json=payload, timeout=30)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    # --- Products ---
    def get_products(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/products"
        r = self.session.get(url, timeout=30)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    def create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/products"
        r = self.session.post(url, json=payload, timeout=30)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    # --- Invoices ---
    def get_invoices(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/invoices"
        r = self.session.get(url, timeout=30)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    def create_invoice(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/invoices"
        r = self.session.post(url, json=payload, timeout=60)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.json()

    def get_invoice_pdf(self, invoice_id: str) -> bytes:
        url = f"{self.base_url}/invoices/{invoice_id}/pdf"
        r = self.session.get(url, timeout=60)
        if r.status_code >= 400:
            raise APIError(r.text)
        return r.content
