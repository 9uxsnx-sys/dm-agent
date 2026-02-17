# AI Sales Agent 🤖

A production-ready, multi-platform AI sales assistant that automates customer interactions, order processing, and inventory management across WhatsApp, Instagram, and Facebook Messenger.

## 🌟 Features

- **Multi-Platform Support**: Unified interface for WhatsApp, Instagram, Facebook
- **AI-Powered Conversations**: Natural language understanding for order intent, extraction, and response generation
- **Smart Order Flow**: Guided conversation (Product → Customer Type → Quantity → Confirmation)
- **Dynamic Pricing**: Wholesaler, retailer, and individual pricing tiers
- **Inventory Management**: Real-time stock checking and low-stock alerts
- **Session Management**: Redis-based conversation state across platforms
- **Production-Ready**: Caching, monitoring, rate limiting, and security built-in

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Redis
- PostgreSQL (or SQLite for testing)

### Option 1: Local Development (Docker)

**Run locally with Docker Compose:**
```bash
docker-compose -f docker-compose.local.yml up -d
```

Access:
- App: http://localhost:8000
- n8n: http://localhost:5678 (admin/admin)

**Stop:**
```bash
docker-compose -f docker-compose.local.yml down
```

### Option 2: Deploy to Railway (Free Cloud Hosting)

**1. Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURNAME/dm-agent.git
git push -u origin main
```

**2. Connect to Railway:**
- Go to [railway.app](https://railway.app) → Sign up (free)
- New Project → Deploy from GitHub repo
- Select your `dm-agent` repo
- Railway auto-detects `docker-compose.yml`

**3. Set Environment Variables in Railway Dashboard:**
- `HF_API_KEY` = your HuggingFace API key
- `WEBHOOK_SECRET` = any random string (e.g., `my-secret-key-123`)

**4. Deploy:**
Click "Deploy" — Railway builds and runs all 4 services automatically.

**Note:** Free tier sleeps after ~30 min idle. Visit the URL to wake it up (5-10 sec delay). Data persists.

### Option 3: Install Locally (No Docker)
```bash
git clone https://github.com/9uxsnx-sys/ai-sales-agent.git
cd ai-sales-agent
pip install -r requirements.txt
```

### Configure
Create `.env`:
```bash
DATABASE_URL=sqlite+aiosqlite:///./test.db
REDIS_URL=redis://localhost:6379/0
HF_API_KEY=your-huggingface-api-key-here
ENVIRONMENT=development
```

### Run
```bash
uvicorn app.main:app --reload
```

## 🔧 Using Real LLM (Not Mock)

1. Get HuggingFace API key from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Set in `.env`: `HF_API_KEY=your-huggingface-api-key`
3. Run tests: `pytest tests/`

## 📁 Project Structure
- `app/` - FastAPI, caching, security, monitoring
- `agents/` - Intent, Extraction, Response agents
- `logic/` - Business logic
- `models/` - Database models
- `tests/` - Test suite

MIT License
