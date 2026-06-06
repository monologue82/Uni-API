<div align="right">

[English](README.md) | [简体中文](README.zh-CN.md)

</div>

<br>

<div align="center">

<img src="logo/logo.png" alt="Uni-API" width="320" />

### A unified API gateway for the AI era.

Route, proxy, and manage hundreds of AI providers through a single, self-hosted interface.

---

![License](https://img.shields.io/badge/license-AGPL--3.0-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![Stars](https://img.shields.io/github/stars/monologue82/Uni-API?style=flat-square&color=yellow)
![Issues](https://img.shields.io/github/issues/monologue82/Uni-API?style=flat-square)

</div>

---

## Why Uni-API?

You have an OpenAI key, a Claude key, a Gemini key, a DeepSeek key, a SiliconFlow key... and you keep switching `base_url` and `Authorization` headers in your code. Uni-API puts **all of them behind one endpoint**.

A single self-hosted gateway that:

- Hosts your own `/v1/chat/completions` for every provider you've paid for.
- Encrypts API keys at rest.
- Logs every call (status, latency, route).
- Lets you mint short-lived client keys for your apps — and revoke them anytime.
- Ships a clean Vue 3 admin UI so non-engineers can manage routes without touching the config.

## Highlights

| | |
|---|---|
| **60+ built-in presets** | OpenAI, Anthropic, Google, Azure, DeepSeek, Groq, Mistral, Cohere, xAI, DashScope, Zhipu, Moonshot, Ollama, LM Studio, vLLM, Replicate, and many more. |
| **Transparent proxy** | Request goes in, response comes out — including streaming. No SDK changes needed. |
| **Per-route API key** | Encrypted with Fernet (`cryptography`) before being written to SQLite. |
| **Live model discovery** | Hit *Fetch Models* and the preset pulls the live `/v1/models` list from upstream. |
| **Call logs** | Every request recorded with method, path, status, latency, and request ID. |
| **Multi-user auth** | JWT + bcrypt; first-time setup wizard at `/setup`. |
| **Auto-refresh cache** | In-memory route table refreshes every 30s — DB changes propagate without restart. |
| **Bilingual UI** | English and Simplified Chinese, switchable from the navbar. |

## Architecture

```
+------------------+        +-----------------------+        +-------------------+
|   Your client    |  HTTP  |   Uni-API Gateway     |  HTTP  |   Upstream API    |
|  (any SDK / app) | -----> |  FastAPI + Vue Admin  | -----> |  OpenAI / Claude  |
|                  | <----- |  :8000 + :3000        | <----- |  / Gemini / ...   |
+------------------+        +-----------------------+        +-------------------+
                                       |
                                       v
                              +-------------------+
                              |  SQLite (async)   |
                              |  routes, users,   |
                              |  call_logs, keys  |
                              +-------------------+
```

The gateway is a **transparent reverse proxy**: it rewrites the upstream `base_url` and injects the upstream `Authorization` header, then streams the response back unchanged.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Windows / macOS / Linux

### Windows (one-shot)

```bat
git clone https://github.com/monologue82/Uni-API.git
cd Uni-API
setup.bat
start.bat
```

### macOS / Linux

```bash
git clone https://github.com/monologue82/Uni-API.git
cd Uni-API

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Frontend
cd frontend
npm install
cd ..

# Run (two terminals)
# Terminal 1
cd backend && ../venv/bin/python run.py
# Terminal 2
cd frontend && npm run dev
```

Then open:

- **Admin UI**: <http://localhost:3000>
- **API Docs (Swagger)**: <http://localhost:8000/docs>
- **First-time setup**: <http://localhost:3000/setup>

The setup wizard creates your admin account. After that, sign in and add your first route.

## Configuration

Copy `backend/.env.example` to `backend/.env` and edit:

```env
SECRET_KEY=replace-with-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///data/uniapi.db
UNIAPI_ENCRYPT_KEY=replace-with-fernet-key
```

> Both `SECRET_KEY` and `UNIAPI_ENCRYPT_KEY` are mandatory in production. Generate a Fernet key with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.

## Built-in Presets

The gateway ships with presets for these providers (and you can add custom ones too):

**LLM (OpenAI-compatible)** — OpenAI, DeepSeek, Groq, Mistral, Together, OpenRouter, Perplexity, SiliconFlow, DashScope, Zhipu, Moonshot, MiniMax, 01.AI, StepFun, Baidu Qianfan, xAI, Fireworks, DeepInfra, Novita, Replicate, HuggingFace, Cloudflare Workers AI, Cohere, SambaNova, Lepton, Lambda, Anyscale, Upstage, InternLM, Baichuan, Spark, Doubao, Tencent Hunyuan, Ollama, LM Studio, vLLM.

**LLM (Anthropic-compatible)** — Anthropic Claude.

**LLM (Google)** — Google AI (Gemini), Google Vertex AI.

**LLM (Azure)** — Azure OpenAI.

**AI Image** — Stability AI, Ideogram, Flux API.

**AI Audio** — ElevenLabs, Deepgram, PlayHT.

**AI Video** — Runway, Luma AI.

**AI Embedding** — Voyage AI, Jina AI.

**Developer** — GitHub, GitLab, Bitbucket, Docker Hub, npm Registry.

**Custom** — any HTTP endpoint with your own auth scheme.

## Calling the Gateway

Once a route named `my-openai` is created, call it exactly like you would call OpenAI — just swap the base URL:

```bash
curl http://localhost:8000/api/v1/gateway/my-openai/v1/chat/completions \
  -H "Authorization: Bearer <your-uniapi-client-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

The gateway will inject the upstream key, forward to `https://api.openai.com/v1/chat/completions`, and stream the response back.

## Project Structure

```
Uni-API/
├── backend/
│   ├── app/
│   │   ├── core/            # cache, http client
│   │   ├── middleware/      # auth, error handling
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routers/         # gateway, routes, auth, logs, apikeys
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # api_types, proxy, route_service, crypto
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/             # axios clients
│   │   ├── components/
│   │   ├── i18n/            # en.js, zh.js
│   │   ├── router/
│   │   ├── stores/          # pinia stores
│   │   └── views/           # Dashboard, Routes, Logs, ApiKeys, Setup, Login
│   ├── package.json
│   └── vite.config.js
├── setup.bat                # Windows: install everything
├── start.bat                # Windows: run everything
├── test.bat                 # Windows: run integration tests
├── .gitignore
├── LICENSE
├── README.md
└── README.zh-CN.md
```

## API Surface

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET`  | `/api/v1/health` | — | Liveness probe |
| `POST` | `/api/v1/auth/login` | — | Issue JWT |
| `POST` | `/api/v1/setup` | — | One-time admin creation |
| `GET`  | `/api/v1/routes` | JWT | List routes |
| `POST` | `/api/v1/routes` | JWT | Create route |
| `PATCH`| `/api/v1/routes/{id}` | JWT | Update route |
| `DELETE`| `/api/v1/routes/{id}` | JWT | Delete route |
| `GET`  | `/api/v1/routes/types` | — | List built-in presets |
| `GET`  | `/api/v1/logs` | JWT | Query call logs |
| `GET/POST/DELETE` | `/api/v1/apikeys` | JWT | Manage client API keys |
| `*`    | `/api/v1/gateway/{route}/{path}` | Client Key | Transparent proxy |

## Testing

```bat
:: Windows
test.bat
```

```bash
# macOS / Linux
source venv/bin/activate
cd backend
python tests/test_integration.py
```

The integration suite boots the app, creates a route, calls it through the gateway, and asserts the response.

## Roadmap

- [ ] Per-key rate limiting and quotas
- [ ] Response caching (Redis)
- [ ] Webhooks on upstream errors
- [ ] Docker image + docker-compose
- [ ] Pluggable auth (OIDC, SAML)
- [ ] Per-team route namespaces

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/amazing-thing`)
3. Commit your changes (`git commit -m 'feat: add amazing thing'`)
4. Push to the branch (`git push origin feat/amazing-thing`)
5. Open a Pull Request

## Security

Found a vulnerability? **Please do not file a public issue.** Email `2627641908@qq.com` instead. I'll respond within 48 hours.

## License

[AGPL-3.0](LICENSE) © 2026 monologue82

This project is licensed under the **GNU Affero General Public License v3.0 or later** — a strong copyleft license. In short:

- You can use, modify, and redistribute this code freely.
- If you modify it and **offer it as a network service** (including internal company use), you must publish the complete corresponding source code of your modified version under the same license.
- Commercial proprietary forks are not permitted without open-sourcing your changes.

For the full text, see [LICENSE](LICENSE). For the human-readable summary, see [tl;dr Legal — AGPL-3.0](https://www.tldrlegal.com/license/gnu-affero-general-public-license-v3-agpl-3-0).

---

<div align="center">

If Uni-API saves you a few hours of `base_url`-swapping, a star is appreciated.

</div>
