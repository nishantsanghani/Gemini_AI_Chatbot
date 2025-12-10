import streamlit as st
import google.generativeai as genai

# Print Gemini SDK version
print("Gemini SDK Version:", genai.__version__)

# Configure API Key
API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)

st.title("Gemini AI Chat App")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Correct Model Name
model = genai.GenerativeModel("gemini-1.5-flash")

# Display old messages
for role, content in st.session_state["history"]:
    with st.chat_message(role):
        st.markdown(content)

# Chat Input
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
