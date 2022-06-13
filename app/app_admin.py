import streamlit as st
import firebase_admin
from firebase_admin import db
import pandas as pd
from utils import get_from_rds


def app():
    st.subheader("Admin Dashboard")
    st.write("Most Recent Reviews")

    results = get_from_rds("/reviews")
    entries = results.values()

    df = pd.DataFrame(entries)
    df = df[["review", "sentiment", "category"]]
    df["category"] = df["category"].apply(lambda x: ", ".join(x))
    df.rename(columns={"review": "Review", "sentiment": "Sentiment",
              "category": "Category"}, inplace=True)
    st.dataframe(df)
