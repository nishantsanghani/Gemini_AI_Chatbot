import streamlit as st
import google.generativeai as genai

# Print Gemini SDK version
print("Gemini SDK Version: 0.8.5")

# Directly set API Key (for testing)
API_KEY = "AIzaSyBsJ0s1aWtcFyTTv6C5DXypaTk5gEthtgE"
genai.configure(api_key=API_KEY)

st.title("Gemini AI Chat App")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Use a valid Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

for role, content in st.session_state["history"]:
    with st.chat_message(role):
        st.markdown(content)

if user_input := st.chat_input("Ask Gemini..."):
    st.session_state["history"].append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state["history"].append(("assistant", reply))
