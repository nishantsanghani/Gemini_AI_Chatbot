import streamlit as st
import google.generativeai as genai

# -----------------------------
# 🔑 Gemini API Key
# -----------------------------
API_KEY = "AIzaSyBsJ0s1aWtcFyTTv6C5DXypaTk5gEthtgE"   # Replace with real key
genai.configure(api_key=API_KEY)

st.title("🤖 Gemini AI Chatbot")

# -----------------------------
# 🔍 Auto-detect working model
# -----------------------------
try:
    models = genai.list_models()

    supported_models = [
        m.name for m in models
        if hasattr(m, "supported_generation_methods")
        and "generateContent" in m.supported_generation_methods
    ]

    if not supported_models:
        st.error("❌ No supported models available for your API key.")
        st.stop()

    # Automatically pick first working model
    model_name = supported_models[0]
    model = genai.GenerativeModel(model_name)

except Exception as e:
    st.error(f"❌ Failed to load models: {e}")
    st.stop()

# -----------------------------
# 💬 Chat History
# -----------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

for role, msg in st.session_state["history"]:
    with st.chat_message(role):
        st.markdown(msg)

# -----------------------------
# ✨ Chat Input
# -----------------------------
if user_input := st.chat_input("Ask Gemini..."):
    st.session_state["history"].append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state["history"].append(("assistant", reply))
