import httpx

client = httpx.Client(trust_env=False, timeout=30)

# Test 1: JSONPlaceholder through gateway
print("=== Test 1: JSONPlaceholder (Public API) ===")
r = client.get("http://localhost:8000/api/v1/gateway/jsonplaceholder/todos/1")
print(f"Status: {r.status_code}")
data = r.json()
print(f"Title: {data['title']}")
print(f"Completed: {data['completed']}")
print()

# Test 2: PokeAPI through gateway
print("=== Test 2: PokeAPI (Public API) ===")
r = client.get("http://localhost:8000/api/v1/gateway/pokeapi/pokemon/pikachu")
print(f"Status: {r.status_code}")
data = r.json()
print(f"Name: {data['name']}")
print(f"Types: {[t['type']['name'] for t in data['types']]}")
print()

# Test 3: Xiaomi MiMo - list models
print("=== Test 3: Xiaomi MiMo - List Models ===")
r = client.get("http://localhost:8000/api/v1/gateway/xiaomi-mimo/models")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    models = data.get("data", [])
    print(f"Models loaded: {len(models)}")
    for m in models:
        print(f"  - {m['id']}")
else:
    print(f"Error: {r.text[:300]}")
print()

# Test 4: Xiaomi MiMo - chat completion
print("=== Test 4: Xiaomi MiMo - Chat Completion ===")
r = client.post(
    "http://localhost:8000/api/v1/gateway/xiaomi-mimo/chat/completions",
    json={
        "model": "mimo-v2.5-pro",
        "messages": [{"role": "user", "content": "Say hello and introduce yourself in one sentence."}],
        "max_tokens": 100,
        "temperature": 0.7,
    },
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Model: {data.get('model')}")
    print(f"Response: {data['choices'][0]['message']['content'][:300]}")
else:
    print(f"Error: {r.text[:300]}")

print("\n=== ALL TESTS DONE ===")
