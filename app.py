import os
import streamlit as st
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import tempfile

# --- Load environment variables ---
load_dotenv()

# --- Configuration ---
st.set_page_config(page_title="PDF Question Answering", page_icon="📄", layout="wide")

# --- Google API Key Setup ---
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file!")
    st.info("💡 Please create a .env file with: GOOGLE_API_KEY=your_api_key_here")
    st.stop()

os.environ["GOOGLE_API_KEY"] = google_api_key

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "current_file_hash" not in st.session_state:
    st.session_state.current_file_hash = None

# --- Main App ---
st.title("📄 PDF Question Answering with Google Gemini")
st.markdown("Upload a PDF and ask questions about its content!")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    try:
        # Calculate file hash
        file_content = uploaded_file.read()
        file_hash = hashlib.md5(file_content).hexdigest()

        # Check if new file is uploaded
        if st.session_state.current_file_hash != file_hash:
            with st.spinner("Processing PDF..."):
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file_content)
                    pdf_path = tmp_file.name

                # Vector store path
                vector_store_path = f"faiss_index_{file_hash}"

                # ✅ Load or create FAISS vector store
                if os.path.exists(vector_store_path):
                    st.info("Loading existing vector store...")
                    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                    vector_store = FAISS.load_local(
                        vector_store_path,
                        embeddings,
                        allow_dangerous_deserialization=True
                    )
                else:
                    # Load PDF
                    loader = PyPDFLoader(pdf_path)
                    documents = loader.load()
                    st.info(f"✅ Loaded {len(documents)} pages from PDF")

                    # Split into chunks
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        separators=["\n\n", "\n", " ", ""]
                    )
                    chunks = text_splitter.split_documents(documents)
                    st.info(f"✅ Created {len(chunks)} text chunks")

                    # ✅ Use HuggingFace embeddings (free & local)
                    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                    vector_store = FAISS.from_documents(chunks, embeddings)
                    vector_store.save_local(vector_store_path)
                    st.success("✅ Vector store created and saved using HuggingFace embeddings")

                # Initialize Gemini LLM
                llm = ChatGoogleGenerativeAI(
                 model="gemini-2.5-flash",  # or another supported alias
                 temperature=0.3,
                 convert_system_message_to_human=True
                 )


                # Create conversational retrieval chain
                memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    output_key="answer"
                )

                qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    retriever=vector_store.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 4}
                    ),
                    memory=memory,
                    return_source_documents=True,
                    verbose=False
                )

                # Store in session
                st.session_state.qa_chain = qa_chain
                st.session_state.current_file_hash = file_hash
                st.session_state.chat_history = []

                os.unlink(pdf_path)

        st.success("✅ PDF is ready for questions!")

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        question = st.chat_input("Ask a question about your PDF:")

        if question and st.session_state.qa_chain:
            # User message
            with st.chat_message("user"):
                st.markdown(question)
            st.session_state.chat_history.append({"role": "user", "content": question})

            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.qa_chain.invoke({"question": question})
                        answer = response['answer']
                        source_docs = response.get('source_documents', [])

                        st.markdown(answer)

                        if source_docs:
                            with st.expander(f"📚 View {len(source_docs)} source chunks"):
                                for i, doc in enumerate(source_docs, 1):
                                    st.markdown(f"*Chunk {i}* (Page {doc.metadata.get('page', 'N/A')}):")
                                    st.text(doc.page_content[:300] + "...")
                                    st.divider()

                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

        # Clear conversation
        if st.sidebar.button("🔄 Clear Conversation"):
            st.session_state.chat_history = []
            if st.session_state.qa_chain:
                st.session_state.qa_chain.memory.clear()
            st.rerun()

    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
else:
    st.info("👆 Please upload a PDF file to get started.")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📖 How to use:")
    st.markdown("""
    1. Upload a PDF file  
    2. Wait for processing  
    3. Ask questions  
    4. View answer sources  
    """)

    st.markdown("### 🔑 Get API Key:")
    st.markdown("[Google AI Studio](https://makersuite.google.com/app/apikey)")

    st.markdown("### ⚙ Model Info:")
    st.markdown("""
    - *LLM:* Gemini 2.5 Flash  
    - *Embeddings:* HuggingFace MiniLM  
    - *Vector Store:* FAISS  
    """)