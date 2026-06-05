import httpx
r = httpx.get("http://localhost:8000/api/v1/health", timeout=3)
print(r.status_code, r.json())