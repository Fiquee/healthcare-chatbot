import streamlit as st
from streamlit_chat import message as st_message
import json
import re
import random
from utils import predict_sentiment, predict_category, insert_to_rds

with open("dialog.json", "r") as dialog_file:
    script = json.load(dialog_file)


def generate_reply():
    user_message = st.session_state["input_text"]
    message_index = len(st.session_state["history"])

    review_sentiment = predict_sentiment(user_message)
    review_category = predict_category(user_message)

    data_dict = {"review": user_message,
                 "sentiment": review_sentiment, "category": review_category}

    # TODO: Update whether we want to push on every message or group all reviews and insert at the end.
    # This currently pushes on every message.
    insert_to_rds("/reviews", data_dict)

    if review_sentiment == "positive":
        reply_options = script["positive_reply"]["message"]
        next_reply = random.choice(reply_options)

    elif review_sentiment == "negative":
        reply_options = script["negative_reply"]["message"]
        next_reply = random.choice(reply_options)

    else:
        next_reply = random.choice(["hshshs", "ehhhhh", "naim, nak code", "nepu tolong buatkan makasih",
                                    "haihhhh", "jom fifa, ehhh jap ada update", "aku ni rajin sebenarnya"])

    placeholders = re.findall("\<\w*\>", next_reply)

    if len(placeholders) > 0:
        for placeholder in placeholders:
            placeholder_text = placeholder[1:-1]

            if placeholder_text == "category":
                next_reply = re.sub(
                    placeholder, ", ".join(review_category), next_reply)

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

    st.subheader("ManulBot")

    for chat in st.session_state.history:
        st_message(**chat)  # unpacking

    st.text_input("Type your reply:", key="input_text",
                  on_change=generate_reply)
