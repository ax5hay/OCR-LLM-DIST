"""
OCR-LLM Streamlit Interface
Alternative lightweight UI for the OCR-LLM backend
"""

import streamlit as st
import requests
import json
from datetime import datetime
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="OCR-LLM Chat",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Constants
BACKEND_URL = "http://127.0.0.1:8000"
API_HEALTH = f"{BACKEND_URL}/api/health"
API_MODELS = f"{BACKEND_URL}/api/models"
API_CHAT = f"{BACKEND_URL}/api/chat"
API_UPLOAD = f"{BACKEND_URL}/api/upload"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_status" not in st.session_state:
    st.session_state.backend_status = "checking"
if "available_models" not in st.session_state:
    st.session_state.available_models = []
if "selected_backend" not in st.session_state:
    st.session_state.selected_backend = "lmstudio"

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Backend selection
    st.subheader("Backend")
    backend = st.radio(
        "Select Backend:",
        ["lmstudio", "ollama"],
        key="backend_select",
        help="Choose which AI backend to use"
    )
    st.session_state.selected_backend = backend
    
    # Check backend health
    try:
        response = requests.get(f"{API_HEALTH}?backend={backend}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                st.success("✅ Backend Healthy")
                st.session_state.backend_status = "healthy"
            else:
                st.error("❌ Backend Unhealthy")
                st.session_state.backend_status = "unhealthy"
        else:
            st.error("❌ Backend Error")
            st.session_state.backend_status = "unhealthy"
    except Exception as e:
        st.error(f"❌ Cannot connect to backend")
        st.session_state.backend_status = "unhealthy"
    
    st.divider()
    
    # Model selection
    st.subheader("Model")
    if st.session_state.backend_status == "healthy":
        try:
            response = requests.get(f"{API_MODELS}?backend={backend}")
            models = response.json().get("models", [])
            st.session_state.available_models = models
            
            if models:
                selected_model = st.selectbox(
                    "Available Models:",
                    models,
                    help="Select which model to use for chat"
                )
            else:
                st.warning("No models available")
                selected_model = None
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            selected_model = None
    else:
        st.info("Connect backend to load models")
        selected_model = None
    
    st.divider()
    
    # Parameters
    st.subheader("Parameters")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative, lower = more focused"
    )
    
    top_k = st.slider(
        "Top-K",
        min_value=0,
        max_value=100,
        value=40,
        help="Number of top tokens to consider"
    )
    
    top_p = st.slider(
        "Top-P",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Nucleus sampling parameter"
    )
    
    st.divider()
    
    # File upload
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"],
        help="Upload a document to extract and use as context"
    )
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{API_UPLOAD}", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Document uploaded: {data['filename']}")
                    st.info(f"Content length: {data['length']} characters")
                else:
                    st.error("Failed to upload document")
            except Exception as e:
                st.error(f"Upload error: {str(e)}")
    
    st.divider()
    
    # Clear button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main content
st.title("🤖 OCR-LLM Chat")
st.caption("AI-powered chat with document support")

# Check if ready
if not selected_model:
    st.warning("⚠️ Please ensure backend is running and a model is selected")
else:
    st.success(f"✅ Ready - Using **{selected_model}**")

# Chat messages
st.subheader("Conversation")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input
user_input = st.chat_input(
    "Type your message here...",
    disabled=not selected_model or st.session_state.backend_status != "healthy"
)

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    if selected_model and st.session_state.backend_status == "healthy":
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                params = {
                    "message": user_input,
                    "model": selected_model,
                    "backend": backend,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                }
                
                # Stream the response
                with requests.post(
                    API_CHAT,
                    params=params,
                    stream=True,
                    timeout=300
                ) as response:
                    if response.status_code == 200:
                        for chunk in response.iter_content(decode_unicode=True):
                            if chunk:
                                full_response += chunk
                                message_placeholder.markdown(full_response + "▌")
                        
                        # Final message
                        message_placeholder.markdown(full_response)
                        
                        # Add to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": full_response
                        })
                    else:
                        st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("Backend: OCR-LLM FastAPI")

with col2:
    st.caption("UI: Streamlit")

with col3:
    st.caption(f"Messages: {len(st.session_state.messages)}")

