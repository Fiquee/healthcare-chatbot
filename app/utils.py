import firebase_admin
from firebase_admin import db
import json
import spacy
import numpy as np
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

classification_model = spacy.load("../output/model-last/")
sentiment_model = spacy.load("../output_sentiment/model-last/")

db_url = os.environ.get("FIRESTORE_URL")
service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

if not firebase_admin._apps:
    cred_object = firebase_admin.credentials.Certificate(
        service_account_path)
    default_app = firebase_admin.initialize_app(cred_object, {
        'databaseURL': db_url})


def insert_to_rds(reference, data):
    ref = db.reference(reference)
    ref.push().set(data)


def get_from_rds(reference):
    ref = db.reference(reference)
    results = ref.get()

    return results


def clean_text(text):
    nlp = spacy.load('en_core_web_sm', disable=[
        'parser', 'ner', 'textcat'])
    text = text.lower()
    doc = nlp(text)

    text = ' '.join(token.lemma_ for token in doc if
                    not token.is_punct
                    and not token.is_currency
                    and not token.is_digit
                    and not token.is_space
                    and not token.is_stop
                    )
    return text


def predict_sentiment(text):
    cleaned_text = clean_text(text)

    doc = sentiment_model(cleaned_text)
    predictions = doc.cats

    return "positive" if predictions["POSITIVE"] > predictions["NEGATIVE"] else "negative"


def predict_category(text):
    cleaned_text = clean_text(text)

    doc = classification_model(cleaned_text)
    predictions = doc.cats

    category_predictions = []

    for key, confidence in predictions.items():
        if confidence > 0.5:
            category_predictions.append(key.lower())

    return category_predictions
