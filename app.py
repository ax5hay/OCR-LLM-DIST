"""
Main Streamlit application for Local Chat.
"""

import sys
import json
import time
import streamlit as st
from datetime import datetime

# Import configuration and utilities
from config import (
    PAGE_ICON,
    PAGE_TITLE,
    DEFAULT_MODEL,
    DEFAULT_TOP_K,
    DEFAULT_TOP_P,
    MODELS_CACHE_TTL,
    ACTIVE_LLM_BACKEND,
    DEFAULT_TEMPERATURE,
)
from services.model_service import run_model
from utils.logging_config import setup_logger
from utils.file_utils import extract_text_from_doc
from services.ollama_service import check_api_health as ollama_health_check, get_available_models as ollama_get_models
from services.lmstudio_service import (
    check_api_health as lmstudio_health_check,
    get_available_models as lmstudio_get_models,
)

# Initialize logger
logger = setup_logger()

# Cache function to improve performance
@st.cache_data(ttl=MODELS_CACHE_TTL)  # Cache available models
def fetch_models(backend: str = "ollama"):
    """
    Cached function to fetch available models from specified backend.
    
    Args:
        backend: Either "ollama" or "lmstudio"
        
    Returns:
        list: Available models or empty list if fetch fails
    """
    if backend == "lmstudio":
        return lmstudio_get_models()
    return ollama_get_models()

def main():
    """Main Streamlit application function."""
    logger.info("Starting application")
    
    try:
        # Configure page
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        
        st.title("🧠 Local Chat (Multi-Backend Support)")
        st.markdown("Chat with selected LLM (Ollama or LMStudio), upload documents (basic OCR), and adjust hyperparameters. More features coming soon.")

        # Backend selection and health check
        selected_backend = st.sidebar.radio(
            "🔌 LLM Backend",
            options=["ollama", "lmstudio"],
            index=0 if ACTIVE_LLM_BACKEND == "ollama" else 1,
            help="Select which local LLM backend to use"
        )
        
        # Update session state for backend
        if "current_backend" not in st.session_state:
            st.session_state.current_backend = selected_backend
        else:
            st.session_state.current_backend = selected_backend
        
        # Check selected backend health
        if selected_backend == "lmstudio":
            api_healthy = lmstudio_health_check()
            if not api_healthy:
                st.error("⚠️ Cannot connect to LMStudio API. Please make sure LMStudio is running on http://127.0.0.1:1234")
                logger.error("LMStudio API health check failed, halting application execution")
                return
            backend_info = "LMStudio (http://127.0.0.1:1234)"
        else:  # ollama
            api_healthy = ollama_health_check()
            if not api_healthy:
                st.error("⚠️ Cannot connect to Ollama API. Please make sure Ollama is running on http://localhost:11434")
                logger.error("Ollama API health check failed, halting application execution")
                return
            backend_info = "Ollama (http://localhost:11434)"
        
        st.sidebar.success(f"✅ Connected to {backend_info}")

        # Set up sidebar for model settings
        model_name, temperature, top_p, top_k = setup_sidebar(selected_backend)
        
        # Document processing section
        document_text = process_document_upload()

        # Chat interface
        setup_chat_interface(model_name, temperature, top_k, top_p, document_text, selected_backend)
    
    except Exception as e:
        logger.exception(f"Critical application error: {str(e)}")
        st.error(f"The application encountered a critical error: {str(e)}")

def setup_sidebar(backend: str):
    """
    Set up the sidebar with model settings and controls.
    
    Args:
        backend: Selected LLM backend ("ollama" or "lmstudio")
    
    Returns:
        tuple: (model_name, temperature, top_p, top_k)
    """
    st.sidebar.header("⚙️ Model Settings")
    
    # Model selection
    try:
        available_models = fetch_models(backend)
        model_name = st.sidebar.selectbox("Select Model", available_models, index=0)
        logger.info(f"Selected model: {model_name} from {backend}")
    except Exception as e:
        logger.exception(f"Error fetching or displaying models: {str(e)}")
        model_name = DEFAULT_MODEL
        st.sidebar.error(f"Error loading models. Using default: {DEFAULT_MODEL}")
    
    # Hyperparameters
    try:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            temperature = st.slider("Temperature", 0.1, 1.0, DEFAULT_TEMPERATURE, 0.05, 
                                  help="Higher values make output more random, lower values more deterministic")
        with col2:
            top_p = st.slider("Top-P", 0.1, 1.0, DEFAULT_TOP_P, 0.05, 
                            help="Nucleus sampling parameter")
        
        # Top-K is not commonly used in LMStudio, but we'll keep it in config
        if backend == "ollama":
            top_k = st.sidebar.slider("Top-K", 1, 100, DEFAULT_TOP_K, 5, 
                                    help="Limits vocabulary to top K tokens")
        else:
            top_k = DEFAULT_TOP_K  # Use default for LMStudio
    except Exception as e:
        logger.exception(f"Error setting up hyperparameter controls: {str(e)}")
        temperature, top_p, top_k = DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K
        st.sidebar.error("Error setting up parameter controls. Using defaults.")
    
    # Log parameter changes
    if "prev_params" not in st.session_state:
        st.session_state.prev_params = {"model": model_name, "temperature": temperature, "top_k": top_k, "top_p": top_p, "backend": backend}
    
    current_params = {"model": model_name, "temperature": temperature, "top_k": top_k, "top_p": top_p, "backend": backend}
    if current_params != st.session_state.prev_params:
        changes = {k: current_params[k] for k in current_params if st.session_state.prev_params[k] != current_params[k]}
        logger.info(f"Parameter changes: {json.dumps(changes)}")
        st.session_state.prev_params = current_params
    
    return model_name, temperature, top_p, top_k

def process_document_upload():
    """
    Handle document upload in the sidebar.
    
    Returns:
        str: Extracted document text or empty string
    """
    st.sidebar.header("📂 Upload Documents")
    
    try:
        uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"], 
                                              help="Upload a document to provide context for your queries")
        
        document_text = ""
        if uploaded_file:
            # Use a status placeholder instead of spinner in sidebar
            status_placeholder = st.sidebar.empty()
            status_placeholder.info("Processing document...")
            
            try:
                logger.info(f"Processing uploaded file: {uploaded_file.name} ({uploaded_file.type})")
                document_text = extract_text_from_doc(uploaded_file)
                
                if document_text.startswith("Error:"):
                    status_placeholder.error(document_text)
                    logger.error(f"Document processing failed: {document_text}")
                else:
                    doc_preview = document_text[:200] + "..." if len(document_text) > 200 else document_text
                    status_placeholder.success(f"Document loaded: {uploaded_file.name}")
                    with st.sidebar.expander("Document Preview"):
                        st.write(doc_preview)
                    logger.success(f"Document loaded successfully: {uploaded_file.name} ({len(document_text)} chars)")
            except Exception as e:
                status_placeholder.error(f"Error processing document: {str(e)}")
                logger.exception(f"Error processing document: {str(e)}")
                document_text = ""
                
        return document_text
    except Exception as e:
        logger.exception(f"Error in file upload section: {str(e)}")
        st.sidebar.error(f"Error processing file upload: {str(e)}")
        return ""

def setup_chat_interface(model_name, temperature, top_k, top_p, document_text, backend: str):
    """
    Set up the chat interface for user interaction.
    
    Args:
        model_name (str): Selected model name
        temperature (float): Temperature parameter
        top_k (int): Top-K parameter
        top_p (float): Top-P parameter
        document_text (str): Extracted document text
        backend (str): LLM backend ("ollama" or "lmstudio")
    """
    # Initialize chat history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Initialized empty chat history")

    # Display chat history
    st.subheader("💬 Chat History")
    
    try:
        chat_container = st.container()
        with chat_container:
            for i, (role, text) in enumerate(st.session_state.chat_history):
                if role == "You":
                    st.info(f"**{role}:** {text}")
                else:
                    st.success(f"**{role}:** {text}")
    except Exception as e:
        logger.exception(f"Error rendering chat history: {str(e)}")
        st.error("Error displaying chat history")
    
    # User input section
    st.subheader("💬 Your Message")
    
    try:
        user_input = st.text_area("Enter your message", height=100, placeholder="Type your message here...")
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            send_button = st.button("Send 🚀", use_container_width=True)
        with col2:
            if st.button("Clear Chat 🗑️", use_container_width=False):
                st.session_state.chat_history = []
                logger.info("Chat history cleared")
                st.experimental_rerun()
        
        if send_button:
            if user_input.strip():
                logger.info(f"User input received ({len(user_input)} chars) via {backend}")
                
                # Append document context if available
                if document_text:
                    final_prompt = f"Document context:\n{document_text}\n\nUser query:\n{user_input}"
                    logger.info(f"Added document context ({len(document_text)} chars) to prompt")
                else:
                    final_prompt = user_input
                
                # Display user message
                st.session_state.chat_history.append(("You", user_input))
                
                # Create a placeholder for the response
                with st.spinner("AI is thinking..."):
                    response_placeholder = st.empty()
                    
                    # Generate response
                    start_time = time.time()
                    full_response = ""
                    
                    try:
                        for chunk in run_model(final_prompt, model_name, temperature, top_k, top_p, backend=backend):
                            full_response += chunk
                            # Update the response in real-time
                            response_placeholder.markdown(f"**AI:** {full_response}▌")
                        
                        elapsed_time = time.time() - start_time
                        logger.success(f"Response generated in {elapsed_time:.2f}s ({len(full_response)} chars) via {backend}")
                        
                        # Update chat history and finalize response
                        st.session_state.chat_history.append(("AI", full_response))
                        response_placeholder.empty()
                        
                        # experimental_rerun to refresh the chat display
                        st.experimental_rerun()
                    except Exception as e:
                        error_msg = str(e)
                        logger.exception(f"Error generating response: {error_msg}")
                        st.error(f"Error generating response: {error_msg}")
            else:
                logger.warning("User attempted to send empty message")
                st.warning("Please enter a message before sending.")
    except Exception as e:
        logger.exception(f"Error in user input section: {str(e)}")
        st.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    try:
        logger.info("Application startup")
        main()
        logger.info("Application executed successfully")
    except Exception as e:
        logger.critical(f"Fatal application error: {str(e)}")
        print(f"FATAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)