import streamlit as st

st.set_page_config(page_title="Janta Seva", layout="wide")

st.title("🇮🇳 Janta Seva App")

# Sidebar
option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Classifier"]
)

# ---------------- CHATBOT ----------------
if option == "Chatbot":
    st.header("Complaint Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Enter your complaint"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # 🔥 MOCK RESPONSE (instead of real model)
        response = "✅ Complaint registered. Our team will resolve it soon."

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


# ---------------- IMAGE CLASSIFIER ----------------
elif option == "Image Classifier":
    st.header("Upload Image")

    file = st.file_uploader("Upload image")

    if file:
        st.image(file)

        # Placeholder prediction
        st.info("🚧 Model is training... prediction coming soon")
