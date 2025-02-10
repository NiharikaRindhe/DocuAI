# import streamlit as st
# import PyPDF2
# import google.generativeai as genai

# # Streamlit UI Config
# st.set_page_config(page_title="📄 DocuAI", layout="wide")

# # Custom CSS for Better Styling
# st.markdown("""
#     <style>
#         .main { background-color: #121212; color: white; }
#         div.stButton > button { width: 100%; border-radius: 12px; font-size: 16px; padding: 10px; }
#         .stTextInput>div>div>input { border-radius: 12px; font-size: 16px; }
#         .chat-container { border: 1px solid #555; padding: 20px; border-radius: 12px; margin-top: 20px; background-color: #1e1e1e; }
#     </style>
# """, unsafe_allow_html=True)

# # Dummy User Credentials
# DUMMY_USER = ".."
# DUMMY_PASSWORD = ".."

# # Initialize session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # Sidebar - Login
# with st.sidebar:
#     st.header("🔑 User Login")
#     if not st.session_state.logged_in:
#         username = st.text_input("👤 Username", key="username")
#         password = st.text_input("🔒 Password", type="password", key="password")

#         if st.button("Login"):
#             if username == DUMMY_USER and password == DUMMY_PASSWORD:
#                 st.session_state.logged_in = True
#                 st.success("✅ Login successful!")
#             else:
#                 st.error("❌ Invalid credentials, try again.")

# # Main Application (Only visible after login)
# if st.session_state.logged_in:
#     st.title("📄 Your document’s AI-powered mind")
#     st.subheader("Upload, analyze, and chat with your document!")

#     # File upload section
#     uploaded_file = st.file_uploader("📂 Upload a PDF Document", type=["pdf"])
#     if uploaded_file:
#         with st.spinner("📖 Extracting text..."):
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             doc_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
#             st.success("✅ Document uploaded successfully!")

#         # Store in session state
#         if "doc_text" not in st.session_state:
#             st.session_state.doc_text = doc_text

#     # Quick Action Buttons
#     st.markdown("### Quick Actions:")
#     with st.container():
#         col1, col2, col3, col4 = st.columns(4, gap="small")
#         with col1:
#             if st.button("📑 Document Analysis", use_container_width=True):
#                 user_query = "Analyze the given document and provide key insights."
#         with col2:
#             if st.button("📝 Summarization", use_container_width=True):
#                 user_query = "Summarize the document in a concise way."
#         with col3:
#             if st.button("💡 Brainstorm", use_container_width=True):
#                 user_query = "Generate creative ideas based on this document."
#         with col4:
#             if st.button("📊 General Analysis", use_container_width=True):
#                 user_query = "Provide a detailed analysis of the document content."

#     # Chat Input Box
#     user_input = st.chat_input("Ask something about the document...")

#     # Streaming Response
#     def stream_gemini_response(prompt):
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt, stream=True)
#         for chunk in response:
#             yield chunk.text

#     if user_input:
#         document_context = st.session_state.doc_text if "doc_text" in st.session_state else ""
#         full_query = f"Document Text:\n{document_context}\n\nUser Query:\n{user_input}"

#         with st.chat_message("user"):
#             st.markdown(user_input)

#         # AI Response Streaming
#         response_container = st.empty()
#         response_text = ""
#         with st.chat_message("assistant"):
#             for chunk in stream_gemini_response(full_query):
#                 response_text += chunk
#                 response_container.markdown(response_text)

#         # Store conversation history
#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         st.session_state.chat_history.append(("user", user_input))
#         st.session_state.chat_history.append(("assistant", response_text))

#     st.markdown('</div>', unsafe_allow_html=True)
# else:
#     st.warning("🔐 Please log in to continue.")


import streamlit as st
import PyPDF2
import google.generativeai as genai

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

# Dummy User Credentials
DUMMY_USER = ".."
DUMMY_PASSWORD = ".."

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# Sidebar - Login
with st.sidebar:
    st.header("🔑 User Login")
    if not st.session_state.logged_in:
        username = st.text_input("👤 Username", key="username")
        password = st.text_input("🔒 Password", type="password", key="password")

        if st.button("Login"):
            if username == DUMMY_USER and password == DUMMY_PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid credentials, try again.")

# Main Application (No login restriction)
st.title("📄 Your Document’s AI-Powered Mind")
st.subheader("Upload, analyze, and chat with your document!")

# File upload section
uploaded_file = st.file_uploader("📂 Upload a PDF Document", type=["pdf"])
if uploaded_file:
    with st.spinner("📖 Extracting text..."):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        doc_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        st.success("✅ Document uploaded successfully!")

    # Store in session state
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
user_query = user_input if user_input else st.session_state.user_query

# Streaming Response Function
def stream_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text

# Check if user entered a query or clicked a button
if user_query:
    document_context = st.session_state.doc_text if "doc_text" in st.session_state else ""
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

    # Clear session state after execution to allow new inputs
    st.session_state.user_query = ""
