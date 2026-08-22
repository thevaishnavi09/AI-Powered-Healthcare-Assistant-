import json
import pickle
import re
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

BASE = Path(__file__).parent
MODEL_DIR = BASE / "model_artifacts"
MODEL_DIR.mkdir(exist_ok=True)

TOKEN_RE = re.compile(r"[a-zA-Z']+")

def tokenize(text):
    return TOKEN_RE.findall(text.lower())

def load_intents():
    with open(BASE / "intents.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_training_data(intents):
    texts, labels = [], []
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            texts.append(pattern)
            labels.append(intent["tag"])
    return texts, labels

def train_and_save():
    intents = load_intents()
    texts, labels = build_training_data(intents)

    vectorizer = CountVectorizer(tokenizer=tokenize)
    X = vectorizer.fit_transform(texts).toarray()

    classes = sorted(set(labels))
    y = tf.keras.utils.to_categorical(
        [classes.index(lbl) for lbl in labels],
        num_classes=len(classes)
    )

    model = Sequential([
        Dense(64, activation="relu", input_shape=(X.shape[1],)),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(len(classes), activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(X, y, epochs=40, batch_size=8, verbose=0)

    model.save(MODEL_DIR / "chatbot_model.keras")

    with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    with open(MODEL_DIR / "classes.pkl", "wb") as f:
        pickle.dump(classes, f)

def load_model_bundle():
    with open(MODEL_DIR / "vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open(MODEL_DIR / "classes.pkl", "rb") as f:
        classes = pickle.load(f)
    model = tf.keras.models.load_model(MODEL_DIR / "chatbot_model.keras")
    return model, vectorizer, classes

def ensure_model():
    if not (MODEL_DIR / "chatbot_model.keras").exists():
        train_and_save()
