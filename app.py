# Your assistant app.py code goes here (re-add if needed after download)
import streamlit as st
import os
import time
from datetime import datetime
from gtts import gTTS
from dotenv import load_dotenv
import openai
import google.generativeai as genai

# === Load API keys ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# === Initialize session states ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "openai"

if "last_queries" not in st.session_state:
    st.session_state.last_queries = []

# === Setup title and toggle ===
st.title("🤖 Your Business AI Assistant")
st.caption("By Vijaychandra - Toggling GPT-3.5 & Gemini with Voice Replies")

col1, col2 = st.columns([1, 2])
with col1:
    model_toggle = st.toggle("Use Gemini instead of ChatGPT")
    st.session_state.model = "gemini" if model_toggle else "openai"

# === Display last 3 conversations ===
st.subheader("💬 Last 3 Conversations")
for q in st.session_state.last_queries[-3:][::-1]:
    st.markdown(f"- {q}")

# === Get user query ===
prompt = st.text_input("Ask something about your business:", key="input")

# === Define response function ===
def get_response_from_openai(prompt):
    messages = st.session_state.messages + [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        reply = response.choices[0].message["content"].strip()
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error: {e}"

def get_response_from_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def speak_text(text):
    tts = gTTS(text=text, lang="en")
    tts.save("reply.mp3")
    st.audio("reply.mp3", format="audio/mp3")

# === On submit ===
if st.button("Submit") and prompt:
    with st.spinner("Thinking..."):
        if st.session_state.model == "openai":
            reply = get_response_from_openai(prompt)
        else:
            reply = get_response_from_gemini(prompt)
        st.success("Here's your assistant's response:")
        st.markdown(reply)
        speak_text(reply)
        st.session_state.last_queries.append(prompt)

# === Reset chat ===
if st.button("🔄 Reset Conversation"):
    st.session_state.messages = []
    st.session_state.last_queries = []
    st.success("Conversation reset.")
