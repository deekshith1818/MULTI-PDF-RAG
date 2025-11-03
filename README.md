# ChatPDF: PDF Question Answering App

This project is a Streamlit web application that allows you to upload PDF files and ask questions about their content. It uses Google Gemini for language understanding and FAISS for efficient document retrieval.

## Features
- Upload multiple PDF files
- Ask questions about the uploaded PDFs
- Uses Google Gemini (via LangChain) for answering questions
- Fast retrieval with FAISS vector store

## Requirements
- Python 3.8+
- Google API Key for Gemini

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Google API Key:**
   - Create a `.env` file in the project root:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **In the web UI:**
   - Upload one or more PDF files using the sidebar
   - Click "Submit" to process the PDFs
   - Ask questions about the content in the main input box

## Notes
- The `faiss_index/` directory is used to store the vector index and is ignored by git.
- Your API key and virtual environment are also ignored by git for security and cleanliness.

## License
MIT License 