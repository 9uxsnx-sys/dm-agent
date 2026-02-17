# Project Structure

## Organization

```
dm-agent/
├── agents/              # AI Agent modules
│   ├── __init__.py
│   ├── intent_agent.py      # Classifies user intent
│   ├── extractor_agent.py   # Extracts product/quantity/customer_type
│   └── response_agent.py    # Generates responses
├── app/                 # FastAPI application
│   ├── __init__.py
│   ├── main.py              # App entry point
│   ├── router.py            # API routes
│   ├── schemas.py           # Pydantic models
│   └── ...
├── db/                  # Database models & seed
│   ├── __init__.py
│   ├── database.py          # SQLAlchemy setup
│   ├── product.py           # Product model
│   ├── customer.py          # Customer model
│   ├── order.py             # Order model
│   └── seed.py              # Mock product seeder
├── logic/               # Business logic
│   ├── __init__.py
│   ├── conversation_engine.py   # Main conversation handler
│   ├── pricing_engine.py        # Price calculations
│   ├── stock_engine.py          # Stock checking
│   └── customer_classifier.py   # Customer type detection
├── n8n/                 # n8n workflow
│   ├── workflow.json          # n8n workflow definition
│   └── README.md              # n8n setup guide
├── prompts/             # LLM prompts
│   ├── intent.txt
│   ├── extract.txt
│   └── response.txt
├── services/            # External services
│   ├── __init__.py
│   └── llm_service.py       # HuggingFace LLM integration
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_basic.py        # Basic import/connection tests
├── docker-compose.yml   # Docker orchestration
├── requirements.txt     # Python dependencies
└── run_tests.py         # Test runner script
```

## Quick Start

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Seed mock products:**
   ```bash
   docker-compose exec app python db/seed.py
   ```

3. **Access n8n (workflow editor):**
   - URL: http://localhost:5678
   - Credentials: admin / admin

4. **Test the agent:**
   ```bash
   curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -d '{"user": "test", "message": "I want to buy headphones", "platform": "web"}'
   ```

## Connections

- **n8n** → **App**: Webhook calls `http://app:8000/webhook`
- **App** → **DB**: PostgreSQL via SQLAlchemy
- **App** → **Redis**: State management & caching
- **Agents** → **LLM Service**: HuggingFace Inference API
- **Logic** → **DB**: Product/Customer/Order queries

## Testing

```bash
# Run tests
python run_tests.py

# Or with pytest directly
pytest tests/ -v
```
