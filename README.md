# 📄 ChatPDF — PDF Question Answering App

A Streamlit web application that lets you upload PDF files and ask questions about their content using **Google Gemini AI**. Built with LangChain and FAISS for fast, accurate document retrieval.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 📤 Upload any PDF file and ask questions about its content
- 🤖 Powered by **Google Gemini 2.5 Flash** for intelligent answers
- 🔍 Fast similarity search using **FAISS** vector store
- 🧠 Conversation memory — follow-up questions remember context
- 📚 View source chunks used to generate each answer
- 💾 Caches processed PDFs so re-uploads are instant

---

## 📋 Prerequisites

Before you begin, make sure you have the following installed on your computer:

### 1. Python (version 3.10 or higher)

- **Download:** https://www.python.org/downloads/
- During installation, **check the box** that says **"Add Python to PATH"**
- To verify installation, open a terminal and run:
  ```bash
  python --version
  ```
  You should see something like `Python 3.13.x`

### 2. Git (optional, for cloning the repo)

- **Download:** https://git-scm.com/downloads
- If you don't want to install Git, you can download the project as a ZIP file instead

### 3. Google API Key (free)

- You'll need a Google API key to use Gemini AI
- Get one for free at: https://makersuite.google.com/app/apikey
- Click **"Create API key"** and copy it somewhere safe

---

## 🚀 Step-by-Step Setup Guide

### Step 1 — Get the Project Files

**Option A: Clone with Git**
```bash
git clone <your-repo-url>
cd MULTI-PDF-RAG
```

**Option B: Download as ZIP**
1. Download the project ZIP file
2. Extract it to a folder on your computer
3. Open a terminal and navigate to that folder:
   ```bash
   cd path/to/MULTI-PDF-RAG
   ```

---

### Step 2 — Create a Virtual Environment

A virtual environment keeps this project's packages separate from your system Python. This avoids conflicts with other projects.

**On Windows (Command Prompt or PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> ✅ You'll know it worked when you see `(venv)` at the beginning of your terminal prompt.

> 💡 **Every time** you open a new terminal to work on this project, you need to activate the virtual environment again using the activate command above.

---

### Step 3 — Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will install all required packages:

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework (the UI) |
| `langchain` | AI orchestration framework |
| `langchain-classic` | Legacy chain & memory support |
| `langchain-community` | Community integrations (PDF loader, FAISS, embeddings) |
| `langchain-google-genai` | Google Gemini integration |
| `langchain-text-splitters` | Splits PDFs into smaller chunks |
| `faiss-cpu` | Fast vector similarity search |
| `pypdf` | PDF file reading |
| `python-dotenv` | Loads API keys from `.env` file |
| `sentence-transformers` | Local embedding model (HuggingFace) |

---

### Step 4 — Set Up Your Google API Key

1. In the project root folder (`MULTI-PDF-RAG`), create a new file called `.env`
2. Open it in any text editor and add this single line:

```env
GOOGLE_API_KEY=your_api_key_here
```

3. Replace `your_api_key_here` with the actual API key you got from [Google AI Studio](https://makersuite.google.com/app/apikey)

> ⚠️ **Important:** Do NOT share your API key or commit the `.env` file to Git. It is already listed in `.gitignore`.

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at **http://localhost:8501**

> 💡 If it doesn't open automatically, copy the URL from the terminal and paste it in your browser.

---

## 📖 How to Use the App

1. **Upload a PDF** — Click the file uploader and select a PDF from your computer
2. **Wait for processing** — The app will read the PDF, split it into chunks, and create a searchable index (this may take a minute the first time)
3. **Ask questions** — Type your question in the chat input at the bottom
4. **View sources** — Click the expandable "View source chunks" section to see which parts of the PDF were used to answer your question
5. **Clear conversation** — Use the "🔄 Clear Conversation" button in the sidebar to start fresh

---

## 🗂️ Project Structure

```
MULTI-PDF-RAG/
├── app.py                # Main application code
├── requirements.txt      # Python dependencies
├── .env                  # Your API key (you create this)
├── .gitignore            # Files ignored by Git
├── README.md             # This file
├── venv/                 # Virtual environment (auto-generated)
└── faiss_index_*/        # Cached vector stores (auto-generated)
```

---

## 🛠️ Troubleshooting

### "GOOGLE_API_KEY not found"
- Make sure you created the `.env` file in the `MULTI-PDF-RAG` folder (not a parent folder)
- Check that the file is named exactly `.env` (not `.env.txt`)
- Verify there are no extra spaces around the `=` sign

### "No module named ..."
- Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
- Re-run: `pip install -r requirements.txt`

### "streamlit: command not found"
- Use the full path instead: `.\venv\Scripts\streamlit.exe run app.py` (Windows)
- Or ensure your virtual environment is activated first

### App is slow on first PDF upload
- This is normal! The first time, it downloads the HuggingFace embedding model (~80MB). Subsequent runs will be much faster since the model is cached locally.

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Google Gemini 2.5 Flash |
| **Embeddings** | HuggingFace MiniLM (sentence-transformers/all-MiniLM-L6-v2) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Framework** | LangChain |
| **PDF Parsing** | PyPDF |

---

## 📄 License

MIT License — feel free to use, modify, and distribute this project.