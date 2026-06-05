import httpx, sys

try:
    r = httpx.get("http://127.0.0.1:8000/api/v1/health", timeout=5)
    print("Health:", r.status_code, r.text)
except Exception as e:
    print("Health FAIL:", e)
    sys.exit(1)

try:
    r = httpx.post("http://127.0.0.1:8000/api/v1/auth/login", 
                   json={"username": "admin", "password": "admin123"},
                   timeout=5)
    print("Login:", r.status_code, r.text[:100])
except Exception as e:
    print("Login FAIL:", e)