# RAG with n8n and Pinecone using Telegram Bot
## Prerequisites
1. *Python* 3
1. *Docker*
2. *NVIDIA Container toolkit*
3. *CUDA 12.X*
4. *cuDNN 9.X*

## How to use
1. **Create `.env` file:**
    ```bash
    N8N_RUNNERS_ENABLED=True
    N8N_WEBHOOK_URL_PROD=${YOUR PRODUCTION URL WEBHOOK FOR TELEGRAM BOT UPDATES}
    N8N_WEBHOOK_URL_TEST=${YOUR TEST URL WEBHOOK FOR TELEGRAM BOT UPDATES}
    TELEGRAM_BOT_TOKEN=${YOUR TELEGRAM BOT TOKEN}
    ```

2. **Start all services**:  
    `docker compose up`

3. **Vectorize and upsert [RAG data](./rag_data/) to Pinecone**:  
    `python load_rag_data.py`

4. **Open n8n in your browser: http://localhost:5678**

5. **Export [workflows](./n8n_workflows/): https://docs.n8n.io/workflows/export-import/#from-the-editor-ui-menu**

6. **Fill your credentials (Google OAuth + TelegramBot token): https://docs.n8n.io/credentials/**

7. **Create spreadsheet on your Google Drive / Google Sheets with next structure**:
    
    * Sheet 1: `history`, columns `[date, user_id, user_request, bot_response, cosine_similarity]`

    * Sheet 2: `errors`, columns: `[workflow_url, error_message, node_with_error, workflow_id, workflow_name]`

    * Sheet 3: `pinecone`, columns: `[date, status]`

8. **Replace cached spreadsheet in all Google Sheet nodes with yours**

9. **Set up your webhook url for trigger node `On message webhook` and match it with `.env`: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/#webhook-urls**

10. **Start chat with your TelegramBot**