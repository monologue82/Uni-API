import asyncio

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

target_app = FastAPI()


@target_app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def echo(path: str, request: Request):
    body = await request.body()
    return JSONResponse({
        "path": f"/{path}",
        "method": request.method,
        "query": str(request.query_params),
        "headers": dict(request.headers),
        "body": body.decode() if body else None,
    })


async def main():
    config = uvicorn.Config(target_app, host="127.0.0.1", port=9999, log_level="error")
    server = uvicorn.Server(config)
    _ = asyncio.create_task(server.serve())
    await asyncio.sleep(1)

    async with httpx.AsyncClient() as client:
        # Check setup status
        r = await client.get("http://localhost:8000/api/v1/setup/status")
        if not r.json()["initialized"]:
            r = await client.post("http://localhost:8000/api/v1/setup/initialize", json={
                "username": "admin",
                "password": "admin123",
            })
            print("Setup initialized:", r.status_code)
            token = r.json()["access_token"]
        else:
            # Login
            r = await client.post("http://localhost:8000/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
            token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Clean up any existing test route (idempotent)
        list_r = await client.get("http://localhost:8000/api/v1/routes", headers=headers)
        for item in list_r.json().get("items", []):
            if item["name"] == "testecho":
                await client.delete(f"http://localhost:8000/api/v1/routes/{item['id']}", headers=headers)
                break

        # Create route
        r = await client.post("http://localhost:8000/api/v1/routes", json={
            "name": "testecho",
            "base_url": "http://127.0.0.1:9999",
            "description": "Local echo server",
            "api_key": "my-secret-key",
            "api_key_header": "X-API-Key",
            "api_key_prefix": "",
            "timeout": 10,
        }, headers=headers)
        print("Create route:", r.status_code)

        # ============ TEST 1: Client provides X-Request-ID ============
        my_request_id = "client-custom-id-12345"
        r = await client.get(
            "http://localhost:8000/api/v1/gateway/testecho/hello",
            headers={"X-Request-ID": my_request_id},
        )
        print("\n=== TEST 1: Client-provided X-Request-ID ===")
        print("Status:", r.status_code)
        print("Response X-Request-ID:", r.headers.get("x-request-id"))
        print("X-UniAPI-Route:", r.headers.get("x-uniapi-route"))
        print("X-UniAPI-Target:", r.headers.get("x-uniapi-target"))
        print("X-UniAPI-Duration-Ms:", r.headers.get("x-uniapi-duration-ms"))

        assert r.headers.get("x-request-id") == my_request_id, f"Request ID mismatch: {r.headers.get('x-request-id')}"
        assert r.headers.get("x-uniapi-route") == "testecho", "Route header missing"
        assert r.headers.get("x-uniapi-target") == "http://127.0.0.1:9999/hello", f"Target mismatch: {r.headers.get('x-uniapi-target')}"
        assert int(r.headers.get("x-uniapi-duration-ms", 0)) >= 0, "Duration header missing"
        print("[PASSED]")

        # Verify the X-Request-ID reached the target API
        data = r.json()
        actual_received_id = data["headers"].get("x-request-id")
        print("Target received X-Request-ID:", actual_received_id)
        assert actual_received_id == my_request_id, f"Target didn't receive our ID: {actual_received_id}"
        print("[PASSED] Target received correct X-Request-ID")

        # ============ TEST 2: No X-Request-ID -> gateway generates one ============
        r = await client.get("http://localhost:8000/api/v1/gateway/testecho/world")
        print("\n=== TEST 2: Auto-generated X-Request-ID ===")
        auto_id = r.headers.get("x-request-id")
        print("Auto-generated X-Request-ID:", auto_id)
        assert auto_id is not None, "Missing auto-generated X-Request-ID"
        assert len(auto_id) == 36, f"UUID4 should be 36 chars, got {len(auto_id)}"
        assert auto_id.count("-") == 4, "Should be UUID4 format"
        print("[PASSED]")

        # Verify target also received it
        data = r.json()
        assert data["headers"].get("x-request-id") == auto_id, "Target didn't receive auto-generated ID"
        print("[PASSED] Target received auto-generated ID")

        # ============ TEST 3: API Key still injected ============
        r = await client.get("http://localhost:8000/api/v1/gateway/testecho/data")
        data = r.json()
        assert data["headers"].get("x-api-key") == "my-secret-key", "API Key not injected"
        print("\n=== TEST 3: API Key injection ===")
        print("[PASSED] API Key still injected correctly")

        # ============ TEST 4: 404 route ============
        r = await client.get("http://localhost:8000/api/v1/gateway/nonexistent/foo")
        print("\n=== TEST 4: 404 route ===")
        print("Status:", r.status_code)
        assert r.status_code == 404
        print("[PASSED] 404 handled")

    print("\n*** ALL TESTS PASSED! ***")
    server.should_exit = True


if __name__ == "__main__":
    asyncio.run(main())
