import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Nova Quantum 1", layout="wide")

st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #1E1E1E; color: #D1D1D1; }
    .stChatMessage { 
        background-color: #2D2D2D !important; 
        border: 1px solid #D4AF37 !important; 
        border-radius: 15px;
        margin-bottom: 20px;
    }
    h1 { color: #D4AF37; text-align: center; letter-spacing: 12px; font-weight: 100; }
    .stChatInputContainer input { 
        background-color: #252526 !important; 
        border: 1px solid #D4AF37 !important; 
        color: white !important;
        border-radius: 10px !important;
    }
    .stChatInputContainer input:disabled { background-color: #121212 !important; opacity: 0.5; }
    </style>
    """, unsafe_allow_html=True)

API_KEY = "AIzaSyCM3Qi_DMfFhkzjQTNUNnzTqUEs1jT_bD4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

if "messages" not in st.session_state: st.session_state.messages = []
if "lock" not in st.session_state: st.session_state.lock = False

st.markdown("<h1>NOVA QUANTUM 1</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسأل nova 1", disabled=st.session_state.lock):
    st.session_state.lock = True
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=None): st.markdown(prompt)
    with st.chat_message("assistant", avatar=None):
        area = st.empty()
        full = ""
        try:
            res = model.generate_content(prompt, stream=True)
            for chunk in res:
                full += chunk.text
                area.markdown(full + " ▌")
                time.sleep(0.005)
            area.markdown(full)
            st.session_state.messages.append({"role": "assistant", "content": full})
        except: st.error("عطل فني.")
    st.session_state.lock = False
    st.rerun()
