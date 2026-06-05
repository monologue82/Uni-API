<div align="right">

[English](README.md) | [简体中文](README.zh-CN.md)

</div>

<br>

<div align="center">

# Uni-API

### 面向 AI 时代的统一 API 网关

通过一个自托管的入口，统一接入、管理、代理数百个 AI 服务。

---

![License](https://img.shields.io/github/license/monologue82/Uni-API?style=flat-square&color=blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?style=flat-square&logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![Stars](https://img.shields.io/github/stars/monologue82/Uni-API?style=flat-square&color=yellow)
![Issues](https://img.shields.io/github/issues/monologue82/Uni-API?style=flat-square)

</div>

---

## 为什么需要 Uni-API？

你手里攥着 OpenAI、Claude、Gemini、DeepSeek、硅基流动……一大堆平台的 API Key，每写一段代码就要切换 `base_url`、改 `Authorization` 头。**Uni-API 把这些全部收拢到一个端点后面**。

一个自托管的网关，可以做到：

- 把所有付费过的服务都挂到你自己的 `/v1/chat/completions` 上
- API Key 在数据库里加密存储
- 每次调用都有日志（状态码、耗时、路由）
- 可以签发可撤销的客户端 Key 给自己的应用
- 自带 Vue 3 后台管理界面，让非工程师也能加路由

## 核心亮点

| | |
|---|---|
| **60+ 内置预设** | OpenAI、Anthropic、Google、Azure、DeepSeek、Groq、Mistral、Cohere、xAI、DashScope、智谱、月之暗面、Ollama、LM Studio、vLLM、Replicate 等等。 |
| **透明代理** | 请求原样进入，响应原样返回，**流式响应也支持**。调用方代码零改动。 |
| **路由级密钥** | 上游 API Key 用 Fernet（`cryptography`）加密后写入 SQLite。 |
| **在线拉取模型列表** | 点一下「拉取模型」，预设会请求上游 `/v1/models` 拿回实时模型清单。 |
| **调用日志** | 每次请求都记录方法、路径、状态码、耗时、请求 ID。 |
| **多用户鉴权** | JWT + bcrypt；首次启动走 `/setup` 向导创建管理员。 |
| **缓存自动刷新** | 内存中的路由表每 30 秒从 DB 同步一次，配置变更无需重启。 |
| **中英双语 UI** | 前端内置中英文，导航栏一键切换。 |

## 架构

```
+------------------+        +-----------------------+        +-------------------+
|     你的客户端     |  HTTP  |    Uni-API 网关        |  HTTP  |     上游 API      |
|  (任意 SDK / 应用) | -----> |   FastAPI + Vue 后台   | -----> | OpenAI / Claude  |
|                  | <----- |    :8000 + :3000       | <----- | / Gemini / ...   |
+------------------+        +-----------------------+        +-------------------+
                                       |
                                       v
                              +-------------------+
                              |   SQLite (异步)    |
                              |  routes / users /  |
                              |  call_logs / keys  |
                              +-------------------+
```

网关本身是一个**透明反向代理**：改写上游 `base_url`、注入上游 `Authorization` 头，然后把响应原样回传。

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Windows / macOS / Linux

### Windows（一条龙）

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

# 后端
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 前端
cd frontend
npm install
cd ..

# 启动（开两个终端）
# 终端 1
cd backend && ../venv/bin/python run.py
# 终端 2
cd frontend && npm run dev
```

启动后访问：

- **管理后台**：<http://localhost:3000>
- **API 文档（Swagger）**：<http://localhost:8000/docs>
- **首次配置**：<http://localhost:3000/setup>

走完初始化向导创建管理员账号，登录后即可添加第一条路由。

## 配置

把 `backend/.env.example` 复制为 `backend/.env` 并修改：

```env
SECRET_KEY=替换成 openssl rand -hex 32 生成的值
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
DEBUG=false
DATABASE_URL=sqlite+aiosqlite:///data/uniapi.db
UNIAPI_ENCRYPT_KEY=替换成 Fernet 密钥
```

> 生产环境 `SECRET_KEY` 和 `UNIAPI_ENCRYPT_KEY` 都要换。Fernet 密钥生成方法：`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`。

## 内置预设

网关自带以下厂商的预设（也支持自定义添加）：

**LLM（OpenAI 兼容）** — OpenAI、DeepSeek、Groq、Mistral、Together、OpenRouter、Perplexity、SiliconFlow、DashScope（阿里百炼）、智谱、月之暗面、MiniMax、零一万物、阶跃星辰、百度千帆、xAI、Fireworks、DeepInfra、Novita、Replicate、HuggingFace、Cloudflare Workers AI、Cohere、SambaNova、Lepton、Lambda、Anyscale、Upstage、书生·浦语、百川、讯飞星火、豆包、腾讯混元、Ollama、LM Studio、vLLM。

**LLM（Anthropic 兼容）** — Anthropic Claude。

**LLM（Google）** — Google AI（Gemini）、Google Vertex AI。

**LLM（Azure）** — Azure OpenAI。

**AI 图像** — Stability AI、Ideogram、Flux API。

**AI 音频** — ElevenLabs、Deepgram、PlayHT。

**AI 视频** — Runway、Luma AI。

**AI 嵌入** — Voyage AI、Jina AI。

**开发者工具** — GitHub、GitLab、Bitbucket、Docker Hub、npm Registry。

**自定义** — 任何 HTTP 端点，自己配鉴权头。

## 调用网关

假设你创建了一条名叫 `my-openai` 的路由，调用方式跟直接调用 OpenAI 一样，**只换 base URL**：

```bash
curl http://localhost:8000/api/v1/gateway/my-openai/v1/chat/completions \
  -H "Authorization: Bearer <你的 Uni-API 客户端 Key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "你好！"}]
  }'
```

网关会自动注入上游 Key，转发到 `https://api.openai.com/v1/chat/completions`，并把响应流式回传。

## 项目结构

```
Uni-API/
├── backend/
│   ├── app/
│   │   ├── core/            # 缓存、HTTP 客户端
│   │   ├── middleware/      # 鉴权、错误处理
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── routers/         # gateway / routes / auth / logs / apikeys
│   │   ├── schemas/         # Pydantic schema
│   │   ├── services/        # api_types / proxy / route_service / crypto
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/             # axios 客户端
│   │   ├── components/
│   │   ├── i18n/            # en.js、zh.js
│   │   ├── router/
│   │   ├── stores/          # pinia store
│   │   └── views/           # Dashboard / Routes / Logs / ApiKeys / Setup / Login
│   ├── package.json
│   └── vite.config.js
├── setup.bat                # Windows：一键安装
├── start.bat                # Windows：一键启动
├── test.bat                 # Windows：跑集成测试
├── .gitignore
├── LICENSE
├── README.md
└── README.zh-CN.md
```

## API 一览

| 方法 | 路径 | 鉴权 | 用途 |
|---|---|---|---|
| `GET`  | `/api/v1/health` | — | 健康检查 |
| `POST` | `/api/v1/auth/login` | — | 颁发 JWT |
| `POST` | `/api/v1/setup` | — | 首次创建管理员 |
| `GET`  | `/api/v1/routes` | JWT | 列出路由 |
| `POST` | `/api/v1/routes` | JWT | 创建路由 |
| `PATCH`| `/api/v1/routes/{id}` | JWT | 更新路由 |
| `DELETE`| `/api/v1/routes/{id}` | JWT | 删除路由 |
| `GET`  | `/api/v1/routes/types` | — | 列出内置预设 |
| `GET`  | `/api/v1/logs` | JWT | 查询调用日志 |
| `GET/POST/DELETE` | `/api/v1/apikeys` | JWT | 管理客户端 API Key |
| `*`    | `/api/v1/gateway/{route}/{path}` | Client Key | 透明代理转发 |

## 运行测试

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

集成测试会启动应用、创建一条路由、穿过网关调用上游，并断言响应正确。

## 路线图

- [ ] 客户端 Key 级别限流和配额
- [ ] 响应缓存（Redis）
- [ ] 上游错误 Webhook 通知
- [ ] Docker 镜像 + docker-compose
- [ ] 可插拔鉴权（OIDC、SAML）
- [ ] 团队级路由命名空间

## 参与贡献

欢迎 PR。重大改动请先开个 Issue 讨论一下。

1. Fork 仓库
2. 新建特性分支（`git checkout -b feat/amazing-thing`）
3. 提交改动（`git commit -m 'feat: add amazing thing'`）
4. 推送到分支（`git push origin feat/amazing-thing`）
5. 发起 Pull Request

## 安全问题

发现漏洞？**请不要公开提 Issue**，直接发邮件到 `2627641908@qq.com`，48 小时内会回复。

## 开源协议

[MIT](LICENSE) © 2026 monologue82

---

<div align="center">

如果 Uni-API 帮你省下了几小时改 `base_url` 的时间，欢迎点个 Star。

</div>
