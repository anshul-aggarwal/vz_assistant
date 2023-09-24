import json
import uuid

import requests
import streamlit as st

st.title("VZ Assistant")

if "key" not in st.session_state:
    st.session_state["key"] = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.write("Session ID: " + st.session_state["key"])


with st.expander("Feedback"):
    thumbs = st.radio(
        "Feedback thumbs up/down",
        [":heavy_minus_sign:", ":thumbsup:", ":thumbsdown:"],
        captions = ["Neutral", "Acceptable", "Not acceptable"], 
        horizontal=True, 
        label_visibility="hidden")

    feedback_text = st.text_input("Feedback")

    st.button("Submit feedback")


# Messages container
with st.container():

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    # Accept user input
    if user_message := st.chat_input():
        # Add user message to chat history

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_message)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                response = requests.get(
                    "http://localhost:8000/query",
                    params={
                        "metadata": "",
                        "session_id": st.session_state["key"],
                        "question": user_message,
                    },
                ).json()
            
            except Exception:
                response = {"content": "hello"}

            assistant_response = response["content"]

            message_placeholder.markdown(assistant_response)
            # Add assistant response to chat history

        st.session_state.messages.append({"role": "user", "message": user_message})
        st.session_state.messages.append(
            {
                "role": "assistant",
                "message": assistant_response,
            }
        )


