import streamlit as st
from streamlit_chat import message as st_message
import json
import re
import random
import pandas as pd
import pyautogui

from utils import predict_sentiment, predict_category, insert_to_rds

with open("dialog.json", "r") as dialog_file:
    script = json.load(dialog_file)


def generate_reply():
    user_message = st.session_state["input_text"]
    message_index = len(st.session_state["history"])

    review_sentiment = predict_sentiment(user_message)
    review_category = predict_category(user_message)

    no_list = ["no", "none", "nope", "that is all", "done"]

    # The reply is not to end the conversation but the categories could not be determined.
    if user_message.lower() not in no_list and len(review_category) == 0:
        reply_options = script["filler_replies"]["message"]
        next_reply = random.choice(reply_options)

    # The reply is to end the conversation.
    elif user_message.lower() in no_list:
        next_reply = script["end_conversation"]["message"][0]
        st.session_state["ended"] = True

    # If there are predicted categories, generate a reply according to both the sentiment and the class.
    if len(review_category) > 0:
        data_dict = {"review": user_message,
                     "sentiment": review_sentiment, "category": review_category}

        if review_sentiment == "positive":
            reply_options = script["positive_reply"]["message"]
            next_reply = random.choice(reply_options)

        elif review_sentiment == "negative":
            reply_options = script["negative_reply"]["message"]
            next_reply = random.choice(reply_options)

        placeholders = re.findall("\<\w*\>", next_reply)

        if len(placeholders) > 0:
            for placeholder in placeholders:
                placeholder_text = placeholder[1:-1]

                if placeholder_text == "category":
                    next_reply = re.sub(
                        placeholder, ", ".join(review_category), next_reply)

        st.session_state.review_list.append(data_dict)

    st.session_state.history.append(
        {"message": user_message, "is_user": True, "key": f"user_{message_index}"})
    st.session_state.history.append(
        {"message": next_reply, "is_user": False, "key": f"bot_{message_index}"})


def app():

    if not st.session_state:
        # Initialise the introduction message
        st.session_state["history"] = [
            {"message": script["greeting"]["message"], "is_user": False}]
        st.session_state["review_list"] = []
        st.session_state["ended"] = False

    for chat in st.session_state.history:
        st_message(**chat)  # unpacking

    if st.session_state["ended"]:
        df = pd.DataFrame(st.session_state["review_list"])
        st.dataframe(df["review"])

        home_button = st.button("Submit and Go Back to Home")

        if home_button:
            for review in st.session_state["review_list"]:
                insert_to_rds("/reviews", review)
            pyautogui.hotkey("ctrl", "F5")

    else:
        st.text_input("Type your reply:", key="input_text",
                      on_change=generate_reply)
