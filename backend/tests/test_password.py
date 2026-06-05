import httpx

client = httpx.Client(trust_env=False)

# Login
r = client.post("http://localhost:8000/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
assert r.status_code == 200, f"Login failed: {r.text}"
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Change password
r = client.put("http://localhost:8000/api/v1/auth/password", json={
    "current_password": "admin123",
    "new_password": "test456789",
}, headers=headers)
print("Change password:", r.status_code, r.json())
assert r.status_code == 200

# Login with new password
r = client.post("http://localhost:8000/api/v1/auth/login", json={"username": "admin", "password": "test456789"})
print("Login (new):", r.status_code)
assert r.status_code == 200

# Change back to original
# Must use the new token (old one might still work since we didn't invalidate)
r = client.put("http://localhost:8000/api/v1/auth/password", json={
    "current_password": "test456789",
    "new_password": "admin123",
}, headers=headers)
print("Revert:", r.status_code, r.json())
assert r.status_code == 200

# Re-login with original password
r = client.post("http://localhost:8000/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
print("Login (original):", r.status_code)
assert r.status_code == 200

# Wrong current password
r = client.put("http://localhost:8000/api/v1/auth/password", json={
    "current_password": "wrongpassword",
    "new_password": "something",
}, headers=headers)
print("Wrong current:", r.status_code, r.json()["detail"])
assert r.status_code == 400

print("\nALL PASSWORD TESTS PASSED")