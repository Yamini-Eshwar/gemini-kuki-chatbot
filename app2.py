import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Gemini AI Chatbot with Memory", page_icon="🤖", layout="wide",  initial_sidebar_state="expanded")

# API Key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Create Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

st.markdown(
    """
    <style>
        body, .stApp{
            background-image: url("https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        }

        [data-testid="stChatInput"] {
            background-color: white;
            color: blue;
            border-radius: 10px;
            padding: 10px;
        }
        [data-testid="stChatInput"] textarea {
            background-color: #E0FEF4;
            color: #000000;
        }
        [data-testid="stChatInput"] textarea::placeholder {
         color: #999999;  /* light gray placeholder */
         font-style: italic;
     }
    
        [data-testid="stSidebar"]{
            background-color: white;
            border-right: 2px solid #C4EDFE;
        }
        .user-bubble{
                background-color: #C4EDFE;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin: 10px;
                width: fit-content;
                max-width: 70%;
                align-self: flex-end;
                font-weight:bold;
        }
        .bot-bubble{
                background-color: #C8F9BB;
                font-weight: bold;
                color: black;
                padding: 10px;
                font-family: Roboto;
                border-radius: 10px;
                margin: 10px;
                width: fit-content;
                max-width: 70%;
                align-self: flex-start;
        }

        .user-bubble, .bot-bubble{
                word-warp: break-word;
                overflow-wrap: break-word;
                
        }
        .chat-container{
                display: flex;
                flex-direction: column;
        }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    # centre the image
    st.markdown(""" 
        <div style="display: flex; justify-content: center;"> 
                <img src="https://chat.kuki.ai/images/meta_kuki_profile.gif", width= "250">
        </div>
    """, unsafe_allow_html=True)
  
    # Sidebar title
    st.markdown("<h1 style='text-align: center;color: #86D3F1'>Kuki Bot</h1>", unsafe_allow_html=True)

     # Stylish buttons
    st.markdown(
        """
        <style>
        .sidebar-button {
            background-color: white;
            color: black;
            border: 1px solid #C4EDFE;
            border-radius: 10px;
            padding: 0.75em 1em;
            width: 100%;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-button">Discord</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-button">Video Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-button" style="margin-bottom: 50px;">About</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 14px; color: gray;">Made with ❤️ by Yamini Krishna</p>', unsafe_allow_html=True)

    
    if st.button("🧹 Clear chat"):
        st.session_state.messages = []

    
# Main area
st.markdown("<h1 style='text-align: center; color:#C4EDFE;font-family: Cursive'>🤖 Gemini AI Chatbot</h1>", unsafe_allow_html=True)


# chat container
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)

# Input box
user_input = st.chat_input("Type your message....")

orders = {
    "12345": "Shipped",
    "67890": "Delivered",
    "11121": "Out for delivery"  
}

if user_input:
    if user_input.lower() == "hi":
        st.image("https://media.giphy.com/media/14aa5GbbHT3bHO/giphy.gif", width=350)

    # 1. save the user message
    st.session_state.messages.append({'role': "user", 'content': user_input})

    # 2. show a spinner while bot is thinking!
    with st.spinner('☁️ Kuki is thinking...'):

        if "track" in user_input.lower():
            order_id = user_input.split()[-1] # assume last word is order number
            status = orders.get(order_id, "Orders not found ❌")
            bot_reply = f"Your order status is: {status}"
        else:
            response = model.generate_content(user_input) # 2. get bot response
            bot_reply = response.text

    # 3. save the bot reply
    st.session_state.messages.append({'role': "bot", 'content': bot_reply})

    st.rerun()