# 🤖 AI FAQ Assistant (PydanticAI + Streamlit)

This is an AI-powered FAQ assistant that answers questions from the DataTalksClub FAQ repository using PydanticAI.

It:

* Fetches and indexes FAQ data from GitHub
* Uses an AI agent to answer questions
* Streams responses in real-time via Streamlit

---

## 🚀 Features

* 🔍 Intelligent search over FAQ data
* ⚡ Streaming responses (ChatGPT-like typing)
* 💬 Interactive chat UI (Streamlit)
* 🧠 PydanticAI agent integration
* 📝 Interaction logging

---

## 📦 Project Structure

```
.
├── app.py              # Streamlit app
├── ingest.py           # Data ingestion + indexing
├── search_agent.py     # PydanticAI agent setup
├── logs.py             # Logging interactions
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone <your-repo-url>
cd <repo>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API key

```bash
export OPENAI_API_KEY=your_key_here
```

**(Windows PowerShell)**

```powershell
setx OPENAI_API_KEY "your_key_here"
```

---

## ▶️ Run the app

```bash
streamlit run app.py
```

---

## 🧠 How it works

### Ingestion

* Downloads markdown files from GitHub
* Filters for relevant FAQ sections
* Builds a searchable index

### Agent

* PydanticAI agent uses the index as context
* Answers user queries

### Streaming

* Uses `agent.run_stream()` to stream responses
* Only the delta (new text) is rendered
