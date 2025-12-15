import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2b313e;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #1e2128;
        margin-right: 20%;
    }
    .message-role {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    # Try to get API key from Streamlit secrets first, then fall back to .env
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it in Streamlit secrets.")
        st.stop()
    
    st.session_state.client = genai.Client(api_key=api_key)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")

# Title
st.title("🤖 Gemini Chat Assistant")
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-role">👤 You</div>
                <div>{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-role">🤖 Gemini</div>
                <div>{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-role">👤 You</div>
            <div>{user_input}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get response from Gemini
    with st.spinner("Thinking..."):
        response_text = ""
        response = st.session_state.chat.send_message_stream(user_input)
        
        # Collect full response
        for chunk in response:
            response_text += chunk.text
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Display assistant message
    st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-role">🤖 Gemini</div>
            <div>{response_text}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Rerun to update the chat
    st.rerun()
