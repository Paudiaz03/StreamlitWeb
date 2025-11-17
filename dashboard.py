import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="✶ UNLIE-One ✶",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Enhanced sophisticated CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Raleway:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Raleway', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
        background-attachment: fixed;
    }
    
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        color: #c8ff00;
        text-align: center;
        font-size: clamp(3rem, 8vw, 5rem);
        margin-bottom: 0.5rem;
        text-shadow: 0 0 50px rgba(200, 255, 0, 0.5);
        animation: elegantGlow 3s ease-in-out infinite alternate;
        font-weight: 400;
        letter-spacing: 0.15em;
    }
    
    @keyframes elegantGlow {
        from { 
            text-shadow: 0 0 30px rgba(200, 255, 0, 0.4),
                         0 0 60px rgba(200, 255, 0, 0.2);
        }
        to { 
            text-shadow: 0 0 50px rgba(200, 255, 0, 0.6),
                         0 0 80px rgba(200, 255, 0, 0.3);
        }
    }
    
    .subtitle {
        font-family: 'Raleway', sans-serif;
        text-align: center;
        color: #999;
        margin-bottom: 3rem;
        font-size: clamp(1.1rem, 3vw, 1.5rem);
        font-weight: 300;
        letter-spacing: 0.35em;
        text-transform: uppercase;
    }
    
    .chat-container {
        max-height: 65vh;
        overflow-y: auto;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(26, 26, 26, 0.5);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #c8ff00, #9fcc00);
        border-radius: 10px;
        border: 2px solid #1a1a1a;
    }
    
    .chat-message {
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        border-radius: 20px;
        animation: elegantSlideIn 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        font-size: 1.25rem;
        line-height: 1.9;
    }
    
    .chat-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg, transparent, rgba(255,255,255,0.05), transparent);
        transform: translateX(-100%);
        transition: transform 0.8s ease;
    }
    
    .chat-message:hover::before {
        transform: translateX(100%);
    }
    
    .chat-message:hover {
        transform: translateX(8px);
        box-shadow: 0 12px 40px rgba(200, 255, 0, 0.15);
    }
    
    .user-msg {
        background: linear-gradient(135deg, #c8ff00 0%, #b8ef00 50%, #a8df00 100%);
        color: #000;
        margin-left: 12%;
        font-weight: 500;
        box-shadow: 0 10px 40px rgba(200, 255, 0, 0.25);
        border: 1px solid rgba(200, 255, 0, 0.3);
    }
    
    .bot-msg {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 50%, #252525 100%);
        color: #e8e8e8;
        margin-right: 12%;
        border: 1px solid #3a3a3a;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
    }
    
    .msg-label {
        font-family: 'Bebas Neue', sans-serif;
        font-weight: 400;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        opacity: 0.85;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    .typing-indicator {
        display: flex;
        gap: 0.5rem;
        padding: 1.2rem 0;
    }
    
    .typing-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #c8ff00;
        animation: elegantTyping 1.6s infinite;
        box-shadow: 0 0 10px rgba(200, 255, 0, 0.5);
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.3s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.6s;
    }
    
    @keyframes elegantTyping {
        0%, 60%, 100% { 
            transform: translateY(0);
            opacity: 0.5;
        }
        30% { 
            transform: translateY(-12px);
            opacity: 1;
        }
    }
    
    @keyframes elegantSlideIn {
        from { 
            opacity: 0; 
            transform: translateY(40px) scale(0.96);
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
    }
    
    .stTextInput input {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%) !important;
        border: 2px solid #3a3a3a !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1.2rem !important;
        padding: 1.3rem 1.8rem !important;
        transition: all 0.4s ease !important;
        font-family: 'Raleway', sans-serif !important;
        letter-spacing: 0.02em !important;
    }
    
    .stTextInput input:focus {
        border-color: #c8ff00 !important;
        box-shadow: 0 0 30px rgba(200, 255, 0, 0.3),
                    0 0 60px rgba(200, 255, 0, 0.1) !important;
        transform: translateY(-3px) !important;
        background: linear-gradient(135deg, #202020 0%, #2a2a2a 100%) !important;
    }
    
    .stTextInput input::placeholder {
        color: #666 !important;
        font-style: italic !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #c8ff00 0%, #b8ef00 50%, #9fcc00 100%) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.2rem 2.8rem !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        width: 100% !important;
        box-shadow: 0 6px 25px rgba(200, 255, 0, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        font-family: 'Bebas Neue', sans-serif !important;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: translate(-50%, -50%);
        transition: width 0.7s, height 0.7s;
    }
    
    .stButton button:hover::before {
        width: 350px;
        height: 350px;
    }
    
    .stButton button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 12px 40px rgba(200, 255, 0, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-2px) scale(0.99) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
        border-right: 1px solid #3a3a3a;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Bebas Neue', sans-serif;
        color: #c8ff00;
        text-shadow: 0 0 25px rgba(200, 255, 0, 0.3);
        letter-spacing: 0.1em;
        font-size: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 600;
        animation: elegantPulse 2.5s infinite;
        letter-spacing: 0.05em;
    }
    
    @keyframes elegantPulse {
        0%, 100% { 
            opacity: 1;
            transform: scale(1);
        }
        50% { 
            opacity: 0.8;
            transform: scale(1.02);
        }
    }
    
    .streaming-text {
        animation: fadeInChar 0.15s ease;
    }
    
    @keyframes fadeInChar {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Chat history item */
    .chat-history-item {
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        background: rgba(200, 255, 0, 0.05);
        border: 1px solid rgba(200, 255, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .chat-history-item:hover {
        background: rgba(200, 255, 0, 0.1);
        border-color: rgba(200, 255, 0, 0.3);
        transform: translateX(5px);
    }
    
    .chat-history-item.active {
        background: rgba(200, 255, 0, 0.15);
        border-color: rgba(200, 255, 0, 0.4);
    }
    
    .chat-title {
        font-weight: 500;
        color: #e0e0e0;
        margin-bottom: 0.3rem;
    }
    
    .chat-date {
        font-size: 0.8rem;
        color: #888;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .chat-message {
            margin: 1.5rem 0;
            padding: 1.5rem;
            font-size: 1.1rem;
        }
        
        .user-msg {
            margin-left: 5%;
        }
        
        .bot-msg {
            margin-right: 5%;
        }
        
        h1 {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
            letter-spacing: 0.25em;
        }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Elegant loader */
    .elegant-loader {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 5px solid #2a2a2a;
        border-top-color: #c8ff00;
        animation: elegantSpin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
        margin: 2.5rem auto;
        box-shadow: 0 0 20px rgba(200, 255, 0, 0.2);
    }
    
    @keyframes elegantSpin {
        to { transform: rotate(360deg); }
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #c8ff00 !important;
        font-weight: 600 !important;
        font-family: 'Bebas Neue', sans-serif !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.05rem !important;
        color: #888 !important;
        letter-spacing: 0.05em !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = None
if 'streaming' not in st.session_state:
    st.session_state.streaming = True

def create_new_chat():
    """Create a new chat conversation"""
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.conversations[chat_id] = {
        'messages': [],
        'title': 'New Conversation',
        'created_at': datetime.now().strftime("%B %d, %Y %I:%M %p")
    }
    st.session_state.current_chat_id = chat_id
    return chat_id

def get_current_messages():
    """Get messages from current chat"""
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.conversations:
        return st.session_state.conversations[st.session_state.current_chat_id]['messages']
    return []

def update_chat_title(chat_id, first_message):
    """Update chat title based on first message"""
    if chat_id in st.session_state.conversations:
        # Take first 50 characters of the message as title
        title = first_message[:50] + "..." if len(first_message) > 50 else first_message
        st.session_state.conversations[chat_id]['title'] = title

# Sidebar
with st.sidebar:
    st.markdown("### API Configuration")
    
    api_key_input = st.text_input(
        "Google AI Studio API Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your API key at https://makersuite.google.com/app/apikey"
    )
    
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        if api_key_input:
            try:
                genai.configure(api_key=api_key_input)
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if '-exp' not in m.name.lower():
                            available_models.append(m.name)
                
                if available_models:
                    preferred = [m for m in available_models if 'flash' in m.lower()]
                    st.session_state.model = preferred[0] if preferred else available_models[0]
                    st.success("✓ API Connected")
                    st.markdown(f"<span class='status-badge' style='background: linear-gradient(135deg, #c8ff00, #9fcc00); color: #000;'>Active Model: {st.session_state.model.split('/')[-1]}</span>", unsafe_allow_html=True)
                else:
                    st.error("No models available")
            except Exception as e:
                st.error(f"✗ Error: {str(e)}")
    
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Conversation", use_container_width=True):
        create_new_chat()
        st.rerun()
    
    st.markdown("---")
    
    # Chat History
    st.markdown("### Chat History")
    
    if st.session_state.conversations:
        # Sort conversations by creation time (newest first)
        sorted_chats = sorted(
            st.session_state.conversations.items(),
            key=lambda x: x[0],
            reverse=True
        )
        
        for chat_id, chat_data in sorted_chats:
            active_class = "active" if chat_id == st.session_state.current_chat_id else ""
            if st.button(
                f"💬 {chat_data['title']}\n📅 {chat_data['created_at']}",
                key=f"chat_{chat_id}",
                use_container_width=True
            ):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        
        st.markdown("---")
        
        # Delete current chat button
        if st.session_state.current_chat_id:
            if st.button("🗑️ Delete Current Chat", use_container_width=True):
                del st.session_state.conversations[st.session_state.current_chat_id]
                st.session_state.current_chat_id = None
                if st.session_state.conversations:
                    st.session_state.current_chat_id = list(st.session_state.conversations.keys())[0]
                st.rerun()
    else:
        st.info("No conversations yet. Start a new one!")
    
    st.markdown("---")
    
    # Streaming configuration
    st.markdown("### Streaming Options")
    st.session_state.streaming = st.toggle("Enable streaming responses", value=True, help="Display responses word by word")
    
    st.markdown("---")
    
    st.markdown("""
    **Steps to obtain your API Key:**
    
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Create a new API Key
    4. Copy and paste it above
    """)

# Header
st.markdown("<h1 style='font-size: 150px;'>BEYOND THE LIE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Think • Write • Explore</p>", unsafe_allow_html=True)

# Verify API Key
if not st.session_state.api_key or not st.session_state.model:
    st.warning("⚠ Please configure your API Key in the sidebar to begin your conversation.")
    st.stop()

# Create first chat if none exists
if not st.session_state.conversations:
    create_new_chat()

# Get current messages
current_messages = get_current_messages()

# Chat container
chat_container = st.container()

with chat_container:
    for msg in current_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-msg">
                <div class="msg-label">You</div>
                <div>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-msg">
                <div class="msg-label">✶ ONE</div>
                <div>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Input
st.markdown("---")
user_input = st.text_input(
    "Message",
    placeholder="Ask anything to ONE...",
    key="input_field",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    send_button = st.button("Send", use_container_width=True)

# Process message
if send_button and user_input.strip():
    # Save user message
    current_messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Update chat title if it's the first message
    if len(current_messages) == 1:
        update_chat_title(st.session_state.current_chat_id, user_input)
    
    # Generate response
    try:
        model = genai.GenerativeModel(st.session_state.model)
        
        # Build history
        chat_history = []
        for message in current_messages[:-1]:
            role = "user" if message["role"] == "user" else "model"
            chat_history.append({
                "role": role,
                "parts": [message["content"]]
            })
        
        # Create chat
        chat = model.start_chat(history=chat_history)
        
        if st.session_state.streaming:
            # Streaming response
            with chat_container:
                st.markdown(f"""
                <div class="chat-message user-msg">
                    <div class="msg-label">You</div>
                    <div>{user_input}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Placeholder for streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                # Show typing indicator
                response_placeholder.markdown("""
                <div class="chat-message bot-msg">
                    <div class="msg-label">✶ ONE</div>
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.5)
                
                # Streaming
                response = chat.send_message(user_input, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(f"""
                        <div class="chat-message bot-msg">
                            <div class="msg-label">✶ ONE</div>
                            <div class="streaming-text">{full_response}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.02)
                
                # Save complete response
                current_messages.append({
                    "role": "model",
                    "content": full_response
                })
        else:
            # Normal response
            with st.spinner("Crafting response..."):
                response = chat.send_message(user_input)
                current_messages.append({
                    "role": "model",
                    "content": response.text
                })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"✗ Error: {str(e)}")
        if current_messages and current_messages[-1]["role"] == "user":
            current_messages.pop()

# Elegant footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1rem; font-family: \"Raleway\", sans-serif; letter-spacing: 0.1em;'>"
    "Powered by Google Gemini AI • Crafted by Pau"
    "</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1rem; font-family: \"Raleway\", sans-serif; letter-spacing: 0.1em;'>"
    "UNLIE-ONE can contain errorss"
    "</p>",
    unsafe_allow_html=True
)
