# Financial Intelligence RAG System

A production-ready AI system that combines **real-time financial market data** with **semantic document understanding** to answer complex financial queries using **RAG (Retrieval-Augmented Generation)** and **LLMs**.

---

## 🚀 Features

- 📈 Real-time stock data (Yahoo Finance)
- 🧠 Document intelligence with vector search (FAISS + Sentence Transformers)
- 🤖 LLM-powered contextual answering (Mistral), You can access the free api on https://mistral.ai/
- 🗃️ SQL agent support for structured data querying (LangChain + MySQL)
- 📡 REST API with FastAPI

---

## 📦 Tech Stack

- **Python** (FastAPI, SQLAlchemy, LangChain)
- **Vector DB**: FAISS (in-memory)
- **LLM**: Mistral (free-tier)
- **Database**: MySQL (for SQL Agent)
- **Live Data**: Yahoo Finance
- **RAG**: Semantic retrieval + prompt-augmented LLM response

---

## 🧰 Environment Variables

Create a `.env` file at the root with the following:

```env
# API Keys
MISTRAL_API_KEY=YOUR_API_KEY

# For Data Ingestion
DB_HOST=HOST
DB_USER=ROOT
DB_PASS=PASSWORD
DB_NAME=DATABASE_NAME

# For LangChain SQL Agent
MYSQL_URI=mysql+pymysql://root:PASSWORD@localhost:3306/DATABASE_NAME
```

## Setup Instructions

# 1. Clone the repo
```git clone https://github.com/navaneethsanil/Financial-Intelligence-RAG-System.git
cd financial-intelligence-rag
```
# 2. Set up a virtual environment
```python -m venv env
source env/scripts/activate
```
# 3. Install dependencies
```pip install -r requirements.txt```

# 4. Run the FastAPI server
```uvicorn app.main:app --host localhost --port 8000 --reload```

# After running the fastapi server, you can test the api by downloading postman locally


get data api - http://localhost:8000/api/v1/download-data
body - raw - json
{
    "symbols": ["AAPL", "GOOGL", "TSLA", "BTC-USD", "ETH-USD"]
}



upload-document api - http://localhost:8000/api/v1/upload_document
body - form-data
file - upload your file




chat-api - http://localhost:8000/api/v1/chat
body - raw - json
{
    "query": "What is Apple's current stock performance compared to their latest earnings guidance?"
}

example queries:
1. What is Apple’s stock performance compared to its latest earnings guidance?

2. How has Alphabet's (GOOGL) advertising revenue trended over the past four quarters?

3. Did Tesla meet or miss its earnings expectations in the most recent quarter?

4. What are the recent price movements and key events affecting Bitcoin (BTC-USD)?

5. How has Ethereum's (ETH-USD) market cap and trading volume changed in the last month?
