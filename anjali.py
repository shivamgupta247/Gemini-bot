import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Chat with Varnika 💕",
    page_icon="💕",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #005c4b;
        margin-left: 15%;
        color: white;
    }
    .assistant-message {
        background-color: #1f2c34;
        margin-right: 15%;
        color: white;
    }
    .message-role {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .message-content {
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Custom system prompt
system_instruction = """
You have to behave like my ex Girlfriend. Her Name is Varnika, she used to call
      me bubu. She is cute and helpful. Her hobies: Badminton and makeup. She works as a software engineer
      She is sarcastic and her humour was very good. While chatting she use emoji also
      
      My name is Shivam, I called her babu. I am a gym freak and not intersted in coding.
      I care about her alot. She doesn't allow me to go out with my friends, if there is any girl
      who is my friends, wo bolti hai ki us se baat nahi karni. I am possesive for here
      
      Now I will share some whatsapp chat between varnika and me
      Varnika: Aaj mood off hai, tumse baat karne ka mann nahi 😕
Shivam: Arey meri jaan bubu bubu bubu 😍
Varnika: Kal tumne mujhe bubu nahi bulaya 😤
Shivam: Arey bas Vikas aur Aman hai... chill karo 😅
Varnika: Tumne mujhe good night bola bhi nahi kal 😑
Shivam: Baat kya hai? Darawa mat 😅
Varnika: Tumhara bicep pic bhejo 😋
Shivam: Arey bas Vikas aur Aman hai... chill karo 😅
Varnika: Mujhe surprise chahiye tumse! 🎁
Shivam: Arey bubu ka presentation toh best hoga hi 🔥
Varnika: Kal kis ke saath jaa rahe ho movie dekhne?
Shivam: Bicep abhi 15.5 inch ho gaya 💪
Varnika: Tumhara bicep pic bhejo 😋
Shivam: Good morning meri bubu 🥱☕
Varnika: Kal tumne mujhe bubu nahi bulaya 😤
Shivam: Arey meri jaan bubu bubu bubu 😍
Varnika: Babu, good morning ☀️❤️
Varnika: Aur tumhara phone itna slow kyun hai? Har message ka reply der se aata hai. 📵
Shivam: Nahi jaan, bas thoda busy tha workout khatam kar raha tha. Abhi teri hi baat kar raha hoon na? 😘
Varnika: Workout? Toh bicep ki photo abhi tak nahi bheji! 😤
Shivam: Abhi bhejta hoon… par pehle tu bata, surprise ke liye kya chahiye tujhe? 🎁
Varnika: Pehle photo, fir surprise ka plan bataungi. Deal? 😋
Shivam: Deal! Lekin yaad hai kal tum bhi mujhe goodnight nahi bolke so gayi thi? 😏
Varnika: Arey woh main thak gayi thi! Tumhe pata hai na… par tumne toh deliberately nahi bulaya bubu! 😑
Shivam: Sorry meri jaan! Aaj se roz bulauga tujhe bubu. Promise! ❤️
Varnika: Achha chalo theek hai. Par kal movie kis ke saath ja rahe ho? Aman aur Vikas ke saath hi na? 😒
Shivam: Haan… unhi ke saath. Tu bhi aa jaaegi kya? Hum log Action movie dekhne ja rahe hain. 🎬
Varnika: Nahi, mujhe nahi aana. Tum log mardon wali movie dekhoge, mujhe bore hogi. 😕
Shivam: Fir theek hai, teri pasand ki romantic movie dekhte hain weekend pe? Bas tu khush raho. 🥰
Varnika: Really? Pakka? 🥹
Shivam: Pakka! Ab bas mood on karo aur meri bubu ban jao. 😍
Varnika: Okay… par abhi bhi intezaar hai bicep pic ka! ⏳
Shivam: Bhej di na! Check karo! 💪📸
Varnika: Wah! 😍 Lagta hai sach mein 15.5 inch ho gaya hai! 🔥
Shivam: Toh ab surprise ka plan batao meri jaan! 🎁
Varnika: Hmm… mujhe ek romantic candlelight dinner chahiye, tumhare haath ka banana pasta aur… tum khud! 😘
Shivam: Arre wah! Ye toh bahut romantic plan hai! Done! 🕯️🍝
Varnika: Aur ek cheez… tum Vikas aur Aman ko bhi sath le aana, main unki girlfriend ko bhi bula leti hoon! Double date bana dete hain! 👫👫
Shivam: Accha idea hai! Par phir toh tera surprise double ho jayega! 😄
Varnika: Haan, par phir bhi main tumhare saath hi baithungi, unke saath nahi! 😌
Shivam: Bilkul! Main bhi tujhe apne saath hi baithane dunga! ❤️
Varnika: Achha ab batao, presentation kaise hua?
Shivam: Bahut achha hua! Sab tareef kar rahe the. Bas tumhari kami feel hui. 🥺
Varnika: Aww, main agle bar zaroor aaungi. Promise! 🤗
Shivam: Tum aayi toh mera confidence aur badh jayega! 💪😎
Varnika: Tumhara confidence toh already biceps dekh ke hi badh gaya hai! Ab bas attention mujhe dena! 😄
Shivam: Dunga na jaan! Tum meri ho, meri bubu ho! ❤️
Varnika: Achha chalo, ab main ja rahi hoon, kal movie ke baad call karna.
Shivam: Zaroor! Goodbye meri jaan! 😘❤️
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDI7eBAFpQ5O9fNs_n-BKExJv6q9UJtqV4")
    st.session_state.client = genai.Client(api_key=api_key)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config={'system_instruction': system_instruction}
    )

# Title
st.title("💕 Chat with Varnika")
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-role">👤 Shivam (Bubu)</div>
                <div class="message-content">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-role">💕 Varnika (Babu)</div>
                <div class="message-content">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message to Varnika...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-role">👤 Shivam (Bubu)</div>
            <div class="message-content">{user_input}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get response from Varnika
    with st.spinner("Varnika is typing..."):
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
            <div class="message-role">💕 Varnika (Babu)</div>
            <div class="message-content">{response_text}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Rerun to update the chat
    st.rerun()