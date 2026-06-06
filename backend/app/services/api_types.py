"""
API type presets with model listing support.
Each preset can have:
  - models_endpoint: path to fetch available models (e.g. "/v1/models")
  - models_key: JSON path to extract model IDs (e.g. "data.*.id")
"""

API_TYPE_PRESETS = [
    # ================================================================
    #  LLM — OpenAI Compatible
    # ================================================================
    {"id": "openai", "name": "OpenAI", "base_url": "https://api.openai.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "GPT-4o, GPT-4.1, o3, o4-mini", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "deepseek", "name": "DeepSeek", "base_url": "https://api.deepseek.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "DeepSeek-V4, DeepSeek-R1", "models_endpoint": "/models", "models_key": "data.*.id"},
    {"id": "groq", "name": "Groq", "base_url": "https://api.groq.com/openai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Llama 4, Mixtral, Gemma (极速推理)", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "mistral", "name": "Mistral AI", "base_url": "https://api.mistral.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Mistral Large, Codestral, Pixtral", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "together", "name": "Together AI", "base_url": "https://api.together.xyz", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "200+ 开源模型", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "openrouter", "name": "OpenRouter", "base_url": "https://openrouter.ai/api", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "统一接入 300+ 模型", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "perplexity", "name": "Perplexity", "base_url": "https://api.perplexity.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "在线搜索增强 LLM", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "siliconflow", "name": "SiliconFlow (硅基流动)", "base_url": "https://api.siliconflow.cn", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "DeepSeek, Qwen, FLUX", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "dashscope", "name": "DashScope (阿里百炼)", "base_url": "https://dashscope.aliyuncs.com/compatible-mode", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Qwen3, Qwen-VL, Llama", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "zhipu", "name": "Zhipu AI (智谱)", "base_url": "https://open.bigmodel.cn/api/paas/v4", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "GLM-4 系列, CogVideoX", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "moonshot", "name": "Moonshot (月之暗面)", "base_url": "https://api.moonshot.cn", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Kimi (128k 上下文)", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "minimax", "name": "MiniMax", "base_url": "https://api.minimax.chat", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "MiniMax-M1, abab 系列", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "yi", "name": "01.AI (零一万物)", "base_url": "https://api.lingyiwanwu.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Yi-Lightning, Yi-Large", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "stepfun", "name": "StepFun (阶跃星辰)", "base_url": "https://api.stepfun.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Step-2 系列", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "baidu_qianfan", "name": "Baidu Qianfan (百度千帆)", "base_url": "https://aip.baidubce.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "ERNIE 4.5, Llama", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "xai", "name": "xAI (Grok)", "base_url": "https://api.x.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Grok-3, Grok-3-mini", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "fireworks", "name": "Fireworks AI", "base_url": "https://api.fireworks.ai/inference", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "120+ 模型, 快速推理", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "deepinfra", "name": "DeepInfra", "base_url": "https://api.deepinfra.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Llama 4, Qwen3, Mixtral", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "novita", "name": "Novita AI", "base_url": "https://api.novita.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "高性价比模型 API", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "replicate", "name": "Replicate", "base_url": "https://api.replicate.com", "api_key_header": "Authorization", "api_key_prefix": "Token ", "category": "LLM (OpenAI)", "format": "openai", "description": "云端托管 ML 模型", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "huggingface", "name": "HuggingFace", "base_url": "https://api-inference.huggingface.co", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "HuggingFace Inference API", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "cloudflare", "name": "Cloudflare Workers AI", "base_url": "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Llama, Mistral, Phi (无服务器)", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "cohere", "name": "Cohere", "base_url": "https://api.cohere.com/v2", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Command A, Command R+, Embed", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "sambanova", "name": "SambaNova", "base_url": "https://api.sambanova.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "高速推理平台", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "lepton", "name": "Lepton AI", "base_url": "https://api.lepton.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "高性能推理服务", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "lambda", "name": "Lambda Labs", "base_url": "https://api.lambdalabs.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "GPU 云 + 推理 API", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "anyscale", "name": "Anyscale", "base_url": "https://api.endpoints.anyscale.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Ray + 模型推理", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "upstage", "name": "Upstage", "base_url": "https://api.upstage.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Solar Pro 2", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "internlm", "name": "InternLM (书生)", "base_url": "https://internlm-chat.intern-ai.org.cn", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "InternLM3 系列", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "baichuan", "name": "Baichuan (百川)", "base_url": "https://api.baichuan-ai.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "Baichuan4 系列", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "spark", "name": "Spark (讯飞星火)", "base_url": "https://spark-api-open.xf-yun.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "讯飞星火 4.0", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "doubao", "name": "Doubao (豆包)", "base_url": "https://ark.cn-beijing.volces.com/api/v3", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "字节跳动豆包大模型", "models_endpoint": "/models", "models_key": "data.*.id"},
    {"id": "tencent_hunyuan", "name": "Hunyuan (腾讯混元)", "base_url": "https://api.hunyuan.cloud.tencent.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "腾讯混元 Turbo S", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "xiaomi_mimo", "name": "Xiaomi MiMo (小米)", "base_url": "https://api.xiaomimimo.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "MiMo 推理模型 (官方 API)", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "ollama", "name": "Ollama (本地)", "base_url": "http://localhost:11434", "api_key_header": "", "api_key_prefix": "", "category": "LLM (OpenAI)", "format": "openai", "description": "本地 LLM 服务", "models_endpoint": "/api/tags", "models_key": "models.*.name"},
    {"id": "lm_studio", "name": "LM Studio (本地)", "base_url": "http://localhost:1234", "api_key_header": "", "api_key_prefix": "", "category": "LLM (OpenAI)", "format": "openai", "description": "本地 LM Studio 服务", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "vllm", "name": "vLLM (本地)", "base_url": "http://localhost:8000", "api_key_header": "", "api_key_prefix": "", "category": "LLM (OpenAI)", "format": "openai", "description": "高性能本地推理引擎", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "openai_compatible", "name": "自定义 OpenAI 兼容", "base_url": "", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (OpenAI)", "format": "openai", "description": "任意 OpenAI 兼容端点", "models_endpoint": "/v1/models", "models_key": "data.*.id"},

    # ================================================================
    #  LLM — Anthropic Compatible
    # ================================================================
    {"id": "anthropic", "name": "Anthropic (Claude)", "base_url": "https://api.anthropic.com", "api_key_header": "x-api-key", "api_key_prefix": "", "category": "LLM (Anthropic)", "format": "anthropic", "description": "Claude Opus 4, Sonnet 4, Haiku", "models_endpoint": "/v1/models", "models_key": "data.*.id"},
    {"id": "anthropic_compatible", "name": "自定义 Anthropic 兼容", "base_url": "", "api_key_header": "x-api-key", "api_key_prefix": "", "category": "LLM (Anthropic)", "format": "anthropic", "description": "任意 Anthropic 兼容端点", "models_endpoint": "/v1/models", "models_key": "data.*.id"},

    # ================================================================
    #  LLM — Google
    # ================================================================
    {"id": "google_ai", "name": "Google AI (Gemini)", "base_url": "https://generativelanguage.googleapis.com", "api_key_header": "x-goog-api-key", "api_key_prefix": "", "category": "LLM (Google)", "format": "google", "description": "Gemini 2.5 Pro, Flash", "models_endpoint": "/v1beta/models", "models_key": "models.*.name"},
    {"id": "google_vertex", "name": "Google Vertex AI", "base_url": "https://{region}-aiplatform.googleapis.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "LLM (Google)", "format": "google", "description": "Google Cloud Vertex AI", "models_endpoint": "/v1/models", "models_key": "data.*.id"},

    # ================================================================
    #  LLM — Azure
    # ================================================================
    {"id": "azure_openai", "name": "Azure OpenAI", "base_url": "https://{resource}.openai.azure.com", "api_key_header": "api-key", "api_key_prefix": "", "category": "LLM (Azure)", "format": "openai", "description": "Azure 托管 OpenAI 模型", "models_endpoint": "/openai/models", "models_key": "data.*.id"},

    # ================================================================
    #  AI 图像生成
    # ================================================================
    {"id": "stability_ai", "name": "Stability AI", "base_url": "https://api.stability.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 图像", "format": "rest", "description": "SDXL, SD3.5, Stable Image"},
    {"id": "ideogram", "name": "Ideogram", "base_url": "https://api.ideogram.ai", "api_key_header": "Api-Key", "api_key_prefix": "", "category": "AI 图像", "format": "rest", "description": "高质量图像生成"},
    {"id": "flux_api", "name": "Flux API", "base_url": "https://api.bfl.ml", "api_key_header": "X-Key", "api_key_prefix": "", "category": "AI 图像", "format": "rest", "description": "Flux 图像生成模型"},

    # ================================================================
    #  AI 音频 / 语音
    # ================================================================
    {"id": "elevenlabs", "name": "ElevenLabs", "base_url": "https://api.elevenlabs.io", "api_key_header": "xi-api-key", "api_key_prefix": "", "category": "AI 音频", "format": "rest", "description": "AI 语音合成与克隆"},
    {"id": "deepgram", "name": "Deepgram", "base_url": "https://api.deepgram.com", "api_key_header": "Authorization", "api_key_prefix": "Token ", "category": "AI 音频", "format": "rest", "description": "语音识别 API"},
    {"id": "playht", "name": "PlayHT", "base_url": "https://api.play.ht", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 音频", "format": "rest", "description": "AI 语音克隆"},

    # ================================================================
    #  AI 视频
    # ================================================================
    {"id": "runway", "name": "Runway", "base_url": "https://api.dev.runwayml.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 视频", "format": "rest", "description": "Gen-3 Alpha 视频生成"},
    {"id": "luma_ai", "name": "Luma AI", "base_url": "https://api.lumalabs.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 视频", "format": "rest", "description": "Dream Machine 视频生成"},

    # ================================================================
    #  AI 嵌入 / 向量
    # ================================================================
    {"id": "voyage", "name": "Voyage AI", "base_url": "https://api.voyageai.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 嵌入", "format": "rest", "description": "高质量嵌入模型"},
    {"id": "jina", "name": "Jina AI", "base_url": "https://api.jina.ai", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "AI 嵌入", "format": "rest", "description": "嵌入与重排序模型"},

    # ================================================================
    #  Developer
    # ================================================================
    {"id": "github", "name": "GitHub", "base_url": "https://api.github.com", "api_key_header": "Authorization", "api_key_prefix": "token ", "category": "Developer", "format": "rest", "description": "GitHub REST API v3"},
    {"id": "gitlab", "name": "GitLab", "base_url": "https://gitlab.com/api/v4", "api_key_header": "PRIVATE-TOKEN", "api_key_prefix": "", "category": "Developer", "format": "rest", "description": "GitLab REST API"},
    {"id": "bitbucket", "name": "Bitbucket", "base_url": "https://api.bitbucket.org/2.0", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "Developer", "format": "rest", "description": "Bitbucket REST API"},
    {"id": "docker_hub", "name": "Docker Hub", "base_url": "https://hub.docker.com/v2", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "Developer", "format": "rest", "description": "Docker Hub API"},
    {"id": "npm", "name": "npm Registry", "base_url": "https://registry.npmjs.org", "api_key_header": "", "api_key_prefix": "", "category": "Developer", "format": "rest", "description": "npm 包注册表"},
    {"id": "pypi", "name": "PyPI", "base_url": "https://pypi.org", "api_key_header": "", "api_key_prefix": "", "category": "Developer", "format": "rest", "description": "Python 包索引"},

    # ================================================================
    #  支付 / 金融
    # ================================================================
    {"id": "stripe", "name": "Stripe", "base_url": "https://api.stripe.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "支付", "format": "rest", "description": "支付处理 API"},
    {"id": "paypal", "name": "PayPal", "base_url": "https://api.paypal.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "支付", "format": "rest", "description": "PayPal 支付 API"},
    {"id": "wise", "name": "Wise", "base_url": "https://api.wise.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "支付", "format": "rest", "description": "国际汇款 API"},

    # ================================================================
    #  通讯 / 消息
    # ================================================================
    {"id": "telegram_bot", "name": "Telegram Bot", "base_url": "https://api.telegram.org/bot{token}", "api_key_header": "", "api_key_prefix": "", "category": "通讯", "format": "rest", "description": "Telegram Bot API"},
    {"id": "slack", "name": "Slack", "base_url": "https://slack.com/api", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "通讯", "format": "rest", "description": "Slack Web API"},
    {"id": "discord", "name": "Discord", "base_url": "https://discord.com/api/v10", "api_key_header": "Authorization", "api_key_prefix": "Bot ", "category": "通讯", "format": "rest", "description": "Discord Bot API"},
    {"id": "whatsapp", "name": "WhatsApp Business", "base_url": "https://graph.facebook.com/v18.0", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "通讯", "format": "rest", "description": "WhatsApp Business API"},

    # ================================================================
    #  邮件
    # ================================================================
    {"id": "sendgrid", "name": "SendGrid", "base_url": "https://api.sendgrid.com/v3", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "邮件", "format": "rest", "description": "邮件发送 API"},
    {"id": "mailgun", "name": "Mailgun", "base_url": "https://api.mailgun.net/v3", "api_key_header": "Authorization", "api_key_prefix": "Basic ", "category": "邮件", "format": "rest", "description": "邮件发送 API"},
    {"id": "resend", "name": "Resend", "base_url": "https://api.resend.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "邮件", "format": "rest", "description": "现代邮件 API"},

    # ================================================================
    #  CMS / 内容
    # ================================================================
    {"id": "wordpress", "name": "WordPress", "base_url": "https://{site}/wp-json/wp/v2", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "CMS", "format": "rest", "description": "WordPress REST API"},
    {"id": "contentful", "name": "Contentful", "base_url": "https://cdn.contentful.com/spaces/{space_id}", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "CMS", "format": "rest", "description": "无头 CMS API"},
    {"id": "sanity", "name": "Sanity", "base_url": "https://{project}.api.sanity.io/v2024-01-01", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "CMS", "format": "rest", "description": "结构化内容平台"},

    # ================================================================
    #  数据库 / BaaS
    # ================================================================
    {"id": "supabase", "name": "Supabase", "base_url": "https://{project}.supabase.co/rest/v1", "api_key_header": "apikey", "api_key_prefix": "", "category": "数据库", "format": "rest", "description": "Supabase REST API"},
    {"id": "firebase", "name": "Firebase", "base_url": "https://firestore.googleapis.com/v1", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "数据库", "format": "rest", "description": "Firebase REST API"},
    {"id": "planetscale", "name": "PlanetScale", "base_url": "https://api.planetscale.com/v1", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "数据库", "format": "rest", "description": "Serverless MySQL"},
    {"id": "neon", "name": "Neon", "base_url": "https://console.neon.tech/api/v2", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "数据库", "format": "rest", "description": "Serverless Postgres"},
    {"id": "upstash", "name": "Upstash Redis", "base_url": "https://{endpoint}.upstash.io", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "数据库", "format": "rest", "description": "Serverless Redis"},

    # ================================================================
    #  搜索
    # ================================================================
    {"id": "algolia", "name": "Algolia", "base_url": "https://{app}-dsn.algolia.net/1", "api_key_header": "X-Algolia-API-Key", "api_key_prefix": "", "category": "搜索", "format": "rest", "description": "搜索引擎 API"},
    {"id": "serpapi", "name": "SerpAPI", "base_url": "https://serpapi.com", "api_key_header": "", "api_key_prefix": "", "category": "搜索", "format": "rest", "description": "搜索引擎结果 API"},
    {"id": "tavily", "name": "Tavily", "base_url": "https://api.tavily.com", "api_key_header": "", "api_key_prefix": "", "category": "搜索", "format": "rest", "description": "AI 搜索 API"},

    # ================================================================
    #  地图 / 位置
    # ================================================================
    {"id": "google_maps", "name": "Google Maps", "base_url": "https://maps.googleapis.com", "api_key_header": "", "api_key_prefix": "", "category": "地图", "format": "rest", "description": "Google Maps Platform"},
    {"id": "mapbox", "name": "Mapbox", "base_url": "https://api.mapbox.com", "api_key_header": "", "api_key_prefix": "", "category": "地图", "format": "rest", "description": "地图与导航 API"},

    # ================================================================
    #  翻译
    # ================================================================
    {"id": "deepl", "name": "DeepL", "base_url": "https://api-free.deepl.com/v2", "api_key_header": "Authorization", "api_key_prefix": "DeepL-Auth-Key ", "category": "翻译", "format": "rest", "description": "高质量翻译 API"},
    {"id": "google_translate", "name": "Google Translate", "base_url": "https://translation.googleapis.com/language/translate/v2", "api_key_header": "", "api_key_prefix": "", "category": "翻译", "format": "rest", "description": "Google 翻译 API"},

    # ================================================================
    #  分析 / 监控
    # ================================================================
    {"id": "mixpanel", "name": "Mixpanel", "base_url": "https://api.mixpanel.com", "api_key_header": "Authorization", "api_key_prefix": "Basic ", "category": "分析", "format": "rest", "description": "产品分析 API"},
    {"id": "amplitude", "name": "Amplitude", "base_url": "https://api2.amplitude.com", "api_key_header": "Authorization", "api_key_prefix": "Basic ", "category": "分析", "format": "rest", "description": "行为分析 API"},
    {"id": "sentry", "name": "Sentry", "base_url": "https://sentry.io/api/0", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "监控", "format": "rest", "description": "错误监控 API"},
    {"id": "datadog", "name": "Datadog", "base_url": "https://api.datadoghq.com/api/v1", "api_key_header": "DD-API-KEY", "api_key_prefix": "", "category": "监控", "format": "rest", "description": "可观测性平台 API"},

    # ================================================================
    #  CRM
    # ================================================================
    {"id": "salesforce", "name": "Salesforce", "base_url": "https://{instance}.salesforce.com/services/data/v59.0", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "CRM", "format": "rest", "description": "Salesforce REST API"},
    {"id": "hubspot", "name": "HubSpot", "base_url": "https://api.hubapi.com", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "CRM", "format": "rest", "description": "HubSpot CRM API"},
    {"id": "pipedrive", "name": "Pipedrive", "base_url": "https://api.pipedrive.com/v1", "api_key_header": "", "api_key_prefix": "", "category": "CRM", "format": "rest", "description": "销售 CRM API"},

    # ================================================================
    #  云存储
    # ================================================================
    {"id": "cloudflare_r2", "name": "Cloudflare R2", "base_url": "https://{account}.r2.cloudflarestorage.com", "api_key_header": "Authorization", "api_key_prefix": "AWS4-HMAC-SHA256 ", "category": "云存储", "format": "rest", "description": "S3 兼容对象存储"},
    {"id": "uploadthing", "name": "UploadThing", "base_url": "https://api.uploadthing.com", "api_key_header": "x-uploadthing-api-key", "api_key_prefix": "", "category": "云存储", "format": "rest", "description": "文件上传服务"},

    # ================================================================
    #  认证
    # ================================================================
    {"id": "clerk", "name": "Clerk", "base_url": "https://api.clerk.com/v1", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "认证", "format": "rest", "description": "用户认证 API"},
    {"id": "auth0", "name": "Auth0", "base_url": "https://{tenant}.auth0.com/api/v2", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "认证", "format": "rest", "description": "身份认证管理"},

    # ================================================================
    #  自动化 / 工作流
    # ================================================================
    {"id": "zapier", "name": "Zapier", "base_url": "https://hooks.zapier.com", "api_key_header": "", "api_key_prefix": "", "category": "自动化", "format": "rest", "description": "Zapier Webhook"},
    {"id": "make", "name": "Make", "base_url": "https://hook.{region}.make.com", "api_key_header": "", "api_key_prefix": "", "category": "自动化", "format": "rest", "description": "Make Webhook"},
    {"id": "n8n", "name": "n8n", "base_url": "https://{instance}.n8n.cloud/api/v1", "api_key_header": "X-N8N-API-KEY", "api_key_prefix": "", "category": "自动化", "format": "rest", "description": "工作流自动化 API"},

    # ================================================================
    #  公开 API
    # ================================================================
    {"id": "jsonplaceholder", "name": "JSONPlaceholder", "base_url": "https://jsonplaceholder.typicode.com", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "免费模拟 REST API"},
    {"id": "pokeapi", "name": "PokeAPI", "base_url": "https://pokeapi.co/api/v2", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "宝可梦 RESTful API"},
    {"id": "restcountries", "name": "REST Countries", "base_url": "https://restcountries.com", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "国家信息 API"},
    {"id": "openlibrary", "name": "Open Library", "base_url": "https://openlibrary.org", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "图书与作者 API"},
    {"id": "httpbin", "name": "HTTPBin", "base_url": "https://httpbin.org", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "HTTP 请求测试"},
    {"id": "quotable", "name": "Quotable", "base_url": "https://api.quotable.io", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "随机名言 API"},
    {"id": "dictionary", "name": "Dictionary API", "base_url": "https://api.dictionaryapi.dev/api/v2", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "英语词典 API"},
    {"id": "randomuser", "name": "RandomUser", "base_url": "https://randomuser.me/api", "api_key_header": "", "api_key_prefix": "", "category": "公开 API", "format": "rest", "description": "随机用户生成"},

    # ================================================================
    #  数据
    # ================================================================
    {"id": "openweathermap", "name": "OpenWeatherMap", "base_url": "https://api.openweathermap.org", "api_key_header": "", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "天气数据 API"},
    {"id": "nasa", "name": "NASA", "base_url": "https://api.nasa.gov", "api_key_header": "", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "NASA 开放 API"},
    {"id": "exchange_rate", "name": "Exchange Rate API", "base_url": "https://open.er-api.com/v6", "api_key_header": "", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "免费汇率 API"},
    {"id": "newsapi", "name": "News API", "base_url": "https://newsapi.org/v2", "api_key_header": "X-Api-Key", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "全球新闻头条"},
    {"id": "alpha_vantage", "name": "Alpha Vantage", "base_url": "https://www.alphavantage.co/query", "api_key_header": "", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "股票与金融数据"},
    {"id": "finnhub", "name": "Finnhub", "base_url": "https://finnhub.io/api/v1", "api_key_header": "X-Finnhub-Token", "api_key_prefix": "", "category": "数据", "format": "rest", "description": "实时股票数据"},

    # ================================================================
    #  媒体
    # ================================================================
    {"id": "unsplash", "name": "Unsplash", "base_url": "https://api.unsplash.com", "api_key_header": "Authorization", "api_key_prefix": "Client-ID ", "category": "媒体", "format": "rest", "description": "免费高清图片"},
    {"id": "pexels", "name": "Pexels", "base_url": "https://api.pexels.com/v1", "api_key_header": "Authorization", "api_key_prefix": "", "category": "媒体", "format": "rest", "description": "免费图库与视频"},
    {"id": "tmdb", "name": "TMDB", "base_url": "https://api.themoviedb.org/3", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "媒体", "format": "rest", "description": "电影数据库 API"},
    {"id": "spotify", "name": "Spotify", "base_url": "https://api.spotify.com/v1", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "媒体", "format": "rest", "description": "Spotify Web API"},
    {"id": "dog_api", "name": "Dog API", "base_url": "https://api.thedogapi.com/v1", "api_key_header": "x-api-key", "api_key_prefix": "", "category": "媒体", "format": "rest", "description": "狗狗图片 API"},
    {"id": "cat_api", "name": "The Cat API", "base_url": "https://api.thecatapi.com/v1", "api_key_header": "x-api-key", "api_key_prefix": "", "category": "媒体", "format": "rest", "description": "猫咪图片 API"},

    # ================================================================
    #  Custom
    # ================================================================
    {"id": "custom", "name": "自定义", "base_url": "", "api_key_header": "Authorization", "api_key_prefix": "Bearer ", "category": "其他", "format": "rest", "description": "手动配置"},
]


def get_all_types() -> list[dict]:
    """Return all API type presets."""
    return API_TYPE_PRESETS


def get_type_by_id(type_id: str) -> dict | None:
    """Return a single type preset by ID."""
    for t in API_TYPE_PRESETS:
        if t["id"] == type_id:
            return t
    return None
