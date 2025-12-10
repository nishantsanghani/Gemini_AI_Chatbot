import streamlit as st
import google.generativeai as genai

# -----------------------------
# 🔑 Gemini API Key
# -----------------------------
API_KEY = "AIzaSyBsJ0s1aWtcFyTTv6C5DXypaTk5gEthtgE"   # Replace with your real key
genai.configure(api_key=API_KEY)

st.title("🤖 Gemini AI Chatbot (Auto-Model Fix)")

# -----------------------------
# 🔍 Detect Available Models
# -----------------------------
st.write("🔄 Fetching supported models...")

try:
    models = genai.list_models()

    supported_models = []
    for m in models:
        if hasattr(m, "supported_generation_methods") and \
           "generateContent" in m.supported_generation_methods:
            supported_models.append(m.name)

    if not supported_models:
        st.error("❌ No valid models available for your API key.")
        st.stop()

except Exception as e:
    st.error(f"❌ Failed to fetch models: {e}")
    st.stop()

# -----------------------------
# 🎯 Model Selection
# -----------------------------
model_name = st.selectbox("Select a Gemini Model:", supported_models)
model = genai.GenerativeModel(model_name)

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
