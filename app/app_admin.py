import streamlit as st
import firebase_admin
from firebase_admin import db
import pandas as pd
from utils import get_from_rds, highlight_rows
import matplotlib.pyplot as plt
import seaborn as sns


def app():
    st.subheader("Admin Dashboard")
    st.write("Most Recent Reviews")

    results = get_from_rds("/reviews")
    entries = results.values()

    # Show DataFrame of recent reviews and their sentiments.
    df = pd.DataFrame(entries)
    df = df[["review", "sentiment", "category"]]
    df["category"] = df["category"].apply(lambda x: ", ".join(x))
    df.rename(columns={"review": "Review", "sentiment": "Sentiment",
              "category": "Category"}, inplace=True)
    highlighted_df = df.style.apply(highlight_rows, axis=1)
    st.dataframe(highlighted_df)

    # Plot a bar chart of the sentiment distribution.
    st.write("Review Sentiment Distribution Chart")
    fig = plt.figure(figsize=(10, 5))
    sns.countplot(x="Sentiment", data=df)
    st.pyplot(fig)

    st.write("Review Categories Distribution Chart")
    positive_column, negative_column = st.columns(2)

    # Plot a bar chart of the categories for the positive and negative reviews.
    with positive_column:
        positive_reviews = df[df["Sentiment"] == "positive"]
        individual_classes = positive_reviews["Category"].str.split(
            ", ")
        individual_classes = [
            element for sublist in individual_classes for element in sublist]

        fig = plt.figure()
        sns.countplot(x=individual_classes).set(
            title="Positive Review Category Distribution")
        st.pyplot(fig)

    with negative_column:
        negative_reviews = df[df["Sentiment"] == "negative"]
        individual_classes = negative_reviews["Category"].str.split(
            ", ")
        individual_classes = [
            element for sublist in individual_classes for element in sublist]

        fig = plt.figure()
        sns.countplot(x=individual_classes).set(
            title="Negative Review Category Distribution")
        st.pyplot(fig)
