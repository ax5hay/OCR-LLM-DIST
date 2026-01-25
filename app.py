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

# ============================================
# CUSTOM STYLING & THEME
# ============================================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --dark-bg: #0f172a;
        --light-bg: #f8fafc;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 2px solid #6366f1;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Chat container styling */
    .chat-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    /* AI message styling */
    .ai-message {
        background: #f1f5f9;
        color: #1e293b;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 4px solid #10b981;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Model selector styling */
    .model-selector {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 2px solid #e2e8f0;
    }
    
    /* Parameter slider styling */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Input area styling */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .status-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-error {
        background: #fee2e2;
        color: #7f1d1d;
    }
    
    /* Section headers */
    .section-header {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #6366f1;
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
        border-left: 4px solid #6366f1;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Sidebar text color fix */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #f1f5f9;
    }
    
    /* Better spacing */
    .spacer {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache function to improve performance
@st.cache_data(ttl=MODELS_CACHE_TTL)
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
        # ============================================
        # HEADER
        # ============================================
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🧠 Local Chat</h1>
            <p class="header-subtitle">Chat with your local LLM • Document Processing • Real-time Streaming</p>
        </div>
        """, unsafe_allow_html=True)

        # ============================================
        # SIDEBAR - BACKEND SELECTION
        # ============================================
        st.sidebar.markdown("## ⚙️ Configuration")
        
        selected_backend = st.sidebar.radio(
            "🔌 **LLM Backend**",
            options=["ollama", "lmstudio"],
            index=0 if ACTIVE_LLM_BACKEND == "ollama" else 1,
            help="Choose which local LLM backend to use"
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
                st.error("❌ Cannot connect to LMStudio API at http://127.0.0.1:1234")
                logger.error("LMStudio API health check failed")
                return
            backend_info = "LMStudio"
            backend_url = "http://127.0.0.1:1234"
        else:
            api_healthy = ollama_health_check()
            if not api_healthy:
                st.error("❌ Cannot connect to Ollama API at http://localhost:11434")
                logger.error("Ollama API health check failed")
                return
            backend_info = "Ollama"
            backend_url = "http://localhost:11434"
        
        st.sidebar.markdown(f"""
        <div style="background: #065f46; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: center;">
            <span style="color: #d1fae5; font-weight: 600;">✅ Connected</span><br/>
            <span style="color: #a7f3d0; font-size: 0.875rem;">{backend_info}</span>
        </div>
        """, unsafe_allow_html=True)

        # ============================================
        # SIDEBAR - MODEL SETTINGS
        # ============================================
        st.sidebar.markdown("### 🎯 Model Settings")
        
        try:
            available_models = fetch_models(selected_backend)
            if available_models:
                model_name = st.sidebar.selectbox(
                    "📦 Select Model",
                    available_models,
                    index=0,
                    help="Choose the model to use for inference"
                )
                logger.info(f"Selected model: {model_name} from {selected_backend}")
            else:
                st.sidebar.error("No models found. Please download models in your backend.")
                model_name = DEFAULT_MODEL
        except Exception as e:
            logger.exception(f"Error fetching models: {str(e)}")
            model_name = DEFAULT_MODEL
            st.sidebar.error(f"Error loading models: {str(e)}")
        
        # ============================================
        # SIDEBAR - HYPERPARAMETERS
        # ============================================
        st.sidebar.markdown("### 🔧 Parameters")
        
        try:
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                temperature = st.slider(
                    "🌡️ Temperature",
                    min_value=0.1,
                    max_value=1.0,
                    value=DEFAULT_TEMPERATURE,
                    step=0.05,
                    help="Higher = more creative, Lower = more focused"
                )
            
            with col2:
                top_p = st.slider(
                    "📊 Top-P",
                    min_value=0.1,
                    max_value=1.0,
                    value=DEFAULT_TOP_P,
                    step=0.05,
                    help="Nucleus sampling parameter"
                )
            
            if selected_backend == "ollama":
                top_k = st.sidebar.slider(
                    "🎲 Top-K",
                    min_value=1,
                    max_value=100,
                    value=DEFAULT_TOP_K,
                    step=5,
                    help="Limits vocabulary size"
                )
            else:
                top_k = DEFAULT_TOP_K
                
        except Exception as e:
            logger.exception(f"Error setting parameters: {str(e)}")
            temperature, top_p, top_k = DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_TOP_K
            st.sidebar.error("Error setting up parameters")
        
        # ============================================
        # SIDEBAR - DOCUMENT UPLOAD
        # ============================================
        st.sidebar.markdown("### 📂 Documents")
        
        try:
            uploaded_file = st.sidebar.file_uploader(
                "Upload PDF or TXT",
                type=["pdf", "txt"],
                help="Upload a document for context in your queries"
            )
            
            document_text = ""
            if uploaded_file:
                status = st.sidebar.status("Processing...", state="running")
                
                try:
                    logger.info(f"Processing file: {uploaded_file.name}")
                    document_text = extract_text_from_doc(uploaded_file)
                    
                    if document_text.startswith("Error:"):
                        status.update(label="Processing failed", state="error")
                        logger.error(f"Document error: {document_text}")
                    else:
                        doc_preview = document_text[:150] + "..." if len(document_text) > 150 else document_text
                        status.update(label=f"✅ Loaded: {uploaded_file.name}", state="complete")
                        
                        with st.sidebar.expander("👀 Preview"):
                            st.write(doc_preview)
                        
                        logger.success(f"Document loaded: {uploaded_file.name} ({len(document_text)} chars)")
                except Exception as e:
                    status.update(label="Processing failed", state="error")
                    logger.exception(f"Error processing document: {str(e)}")
                    document_text = ""
                    
        except Exception as e:
            logger.exception(f"Error in file upload: {str(e)}")
            st.sidebar.error(f"File upload error: {str(e)}")
            document_text = ""
        
        # ============================================
        # MAIN CONTENT - CHAT INTERFACE
        # ============================================
        setup_chat_interface(model_name, temperature, top_k, top_p, document_text, selected_backend)
    
    except Exception as e:
        logger.exception(f"Critical error: {str(e)}")
        st.error(f"❌ Critical Error: {str(e)}")

def setup_chat_interface(model_name, temperature, top_k, top_p, document_text, backend: str):
    """Set up the beautiful chat interface."""
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Initialized chat history")

    # ============================================
    # CHAT HISTORY DISPLAY
    # ============================================
    st.markdown("### 💬 Conversation")
    
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for role, text in st.session_state.chat_history:
                if role == "You":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong><br/>{text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <strong>🤖 AI:</strong><br/>{text}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Start a conversation by typing a message below!")
    
    st.markdown("---")
    
    # ============================================
    # INPUT AREA
    # ============================================
    st.markdown("### ✍️ Your Message")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Message",
            label_visibility="collapsed",
            placeholder="Type your message here... (shift + enter for new line)",
            height=100
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("🚀 Send", use_container_width=True, key="send")
        clear_button = st.button("🗑️ Clear", use_container_width=True, key="clear")
    
    # ============================================
    # HANDLE USER INPUT
    # ============================================
    if clear_button:
        st.session_state.chat_history = []
        logger.info("Chat cleared")
        st.rerun()
    
    if send_button:
        if user_input.strip():
            logger.info(f"User input: {len(user_input)} chars via {backend}")
            
            # Prepare prompt
            if document_text:
                final_prompt = f"Document context:\n{document_text}\n\nUser query:\n{user_input}"
                logger.info(f"Added document context: {len(document_text)} chars")
            else:
                final_prompt = user_input
            
            # Add user message to history
            st.session_state.chat_history.append(("You", user_input))
            
            # Generate response
            with st.spinner("🤖 AI is thinking..."):
                response_placeholder = st.empty()
                
                start_time = time.time()
                full_response = ""
                
                try:
                    for chunk in run_model(final_prompt, model_name, temperature, top_k, top_p, backend=backend):
                        full_response += chunk
                        response_placeholder.markdown(f"""
                        <div class="ai-message">
                            <strong>🤖 AI:</strong><br/>{full_response}▌
                        </div>
                        """, unsafe_allow_html=True)
                    
                    elapsed = time.time() - start_time
                    logger.success(f"Response in {elapsed:.2f}s ({len(full_response)} chars)")
                    
                    # Add to history
                    st.session_state.chat_history.append(("AI", full_response))
                    response_placeholder.empty()
                    
                    st.rerun()
                    
                except Exception as e:
                    logger.exception(f"Error: {str(e)}")
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please type a message first!")

if __name__ == "__main__":
    try:
        logger.info("App startup")
        main()
        logger.info("App executed successfully")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        print(f"FATAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)


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