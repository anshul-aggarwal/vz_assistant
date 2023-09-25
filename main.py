import os
import uuid
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("VZ Assistant")
st.session_state["authenticated"] = False

if "key" not in st.session_state:
    st.session_state["key"] = str(uuid.uuid4())

if "starttime" not in st.session_state:
    st.session_state["starttime"] = str(datetime.now())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.write("Session ID: " + st.session_state["key"])
st.write("Start Time: " + st.session_state["starttime"])
passcode = st.text_input("Passcode")

if passcode == os.getenv("PASSCODE"):
    st.session_state["authenticated"] = True

with st.expander("Feedback"):
    thumbs = st.radio(
        "Feedback thumbs up/down",
        [":heavy_minus_sign:", ":thumbsup:", ":thumbsdown:"],
        captions = ["Neutral", "Acceptable", "Not acceptable"], 
        horizontal=True, 
        label_visibility="hidden")

    feedback_text = st.text_input("Feedback")

    if st.session_state['authenticated']:
        st.button("Submit feedback")
    else:
        st.button("Submit feedback", disabled=True)

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

            if st.session_state['authenticated']:
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
            else:
                assistant_response = "*Incorrect Passcode. Query Ignored.*"

            message_placeholder.markdown(assistant_response)
            # Add assistant response to chat history

        st.session_state.messages.append({"role": "user", "message": user_message})
        st.session_state.messages.append(
            {
                "role": "assistant",
                "message": assistant_response,
            }
        )


