# n8n Workflow Setup

## Overview
The n8n workflow connects external messaging platforms (WhatsApp, Messenger, etc.) to the AI Sales Agent.

## Workflow File
- **Location**: `n8n/workflow.json`
- **Name**: AI Sales Agent Workflow

## How It Works
1. **Webhook Node**: Receives incoming messages from external platforms
2. **Format Message Node**: Standardizes the message format
3. **AI Agent HTTP Request**: Sends formatted message to the agent at `http://app:8000/webhook`
4. **Respond to Webhook**: Returns the agent's response to the original platform

## Setup Instructions

### 1. Start the Services
```bash
docker-compose up -d
```

### 2. Access n8n
Open http://localhost:5678 in your browser
- Default credentials: admin / admin

### 3. Import the Workflow
1. Go to Workflows → Import from File
2. Select `n8n/workflow.json`
3. Activate the workflow

### 4. Configure External Webhook
The webhook URL for external platforms:
```
http://localhost:5678/webhook/incoming-message
```

## Testing
Send a test message to the webhook:
```bash
curl -X POST http://localhost:5678/webhook/incoming-message \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "Hello", "platform": "web"}'
```

## Connection Flow
```
External Platform → n8n Webhook → AI Agent (app:8000/webhook) → Response
```
