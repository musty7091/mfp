import requests

# FastAPI Backend adresi ve portu
BASE_URL = "http://localhost:8000"

def get_full_url(endpoint: str) -> str:
    """Belirtilen API endpoint'i için tam URL oluşturur."""
    if not endpoint.startswith("/api/v1"):
        endpoint = f"/api/v1{endpoint}"
    return f"{BASE_URL}{endpoint}"

def api_request(method: str, endpoint: str, data: dict = None, headers: dict = None, is_form_data: bool = False):
    """Genel API isteği işleyicisi."""
    url = get_full_url(endpoint)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            # Login endpoint'i için Form verisi, diğerleri için JSON
            if is_form_data:
                # Login için Form verisi gönderimi (OAuth2PasswordRequestForm'a uyum)
                response = requests.post(
                    url, 
                    data={"username": data.get("username"), "password": data.get("password")},
                    headers=headers
                )
            else:
                # Diğer POST istekleri için JSON body gönderimi
                response = requests.post(url, json=data, headers=headers)
        
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Desteklenmeyen HTTP metodu: {method}")

        response.raise_for_status() # HTTP hata kodlarını yakalar (4xx, 5xx)
        return response.json() if response.content else {}

    except requests.exceptions.HTTPError as e:
        # FastAPI'den gelen hata detaylarını yakalamaya çalış
        try:
            error_details = e.response.json()
        except requests.exceptions.JSONDecodeError:
            error_details = {"detail": e.response.text}
            
        return {"error": error_details.get("detail", f"API isteği başarısız oldu: {e.response.status_code}")}
    
    except requests.exceptions.ConnectionError:
        return {"error": "API sunucusuna (Backend) ulaşılamıyor. Çalıştığından emin olun."}
    
    except Exception as e:
        return {"error": f"Beklenmeyen bir hata oluştu: {e}"}