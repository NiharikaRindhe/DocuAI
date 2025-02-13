import streamlit as st
import PyPDF2
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API Key securely
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key is missing. Please set GEMINI_API_KEY in the .env file.")
else:
    genai.configure(api_key=API_KEY)

# Streamlit UI Config
st.set_page_config(page_title="📄 DocuAI", layout="wide")

# Custom CSS for Better Styling
st.markdown("""
    <style>
        .main { background-color: #121212; color: white; }
        div.stButton > button { width: 100%; border-radius: 12px; font-size: 16px; padding: 10px; }
        .stTextInput>div>div>input { border-radius: 12px; font-size: 16px; }
        .chat-container { border: 1px solid #555; padding: 20px; border-radius: 12px; margin-top: 20px; background-color: #1e1e1e; }
    </style>
""", unsafe_allow_html=True)

# Main Application
st.title("📄 Your Document’s AI-Powered Mind")
st.subheader("Upload, analyze, and chat with your document!")

# File upload section
uploaded_file = st.file_uploader("📂 Upload a PDF Document", type=["pdf"])

if uploaded_file:
    with st.spinner("📖 Extracting text..."):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        doc_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        st.success("✅ Document uploaded successfully!")

    # Store document text in session state
    st.session_state.doc_text = doc_text

# Quick Action Buttons
st.markdown("### Quick Actions:")
with st.container():
    col1, col2, col3, col4 = st.columns(4, gap="small")

    with col1:
        if st.button("📑 Document Analysis", use_container_width=True):
            st.session_state.user_query = "Analyze the given document and provide key insights."
    with col2:
        if st.button("📝 Summarization", use_container_width=True):
            st.session_state.user_query = "Summarize the document in a concise way."
    with col3:
        if st.button("💡 Brainstorm", use_container_width=True):
            st.session_state.user_query = "Generate creative ideas based on this document."
    with col4:
        if st.button("📊 General Analysis", use_container_width=True):
            st.session_state.user_query = "Provide a detailed analysis of the document content."

# Chat Input Box
user_input = st.chat_input("Ask something about the document...")
user_query = user_input if user_input else st.session_state.get("user_query", "")

# Streaming Response Function
def stream_gemini_response(prompt):
    if not API_KEY:
        st.error("❌ API Key is missing. Set it in the .env file.")
        return

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return

# Chat Processing
if user_query:
    document_context = st.session_state.get("doc_text", "")
    full_query = f"Document Text:\n{document_context}\n\nUser Query:\n{user_query}"

    with st.chat_message("user"):
        st.markdown(user_query)

    # AI Response Streaming
    response_container = st.empty()
    response_text = ""
    with st.chat_message("assistant"):
        for chunk in stream_gemini_response(full_query):
            response_text += chunk
            response_container.markdown(response_text)

    # Store conversation history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append(("user", user_query))
    st.session_state.chat_history.append(("assistant", response_text))

    # Reset session query
    st.session_state.user_query = ""


#     # Reset session query
#     st.session_state.user_query = ""
