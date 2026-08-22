import json
import random
from pathlib import Path

from model_utils import ensure_model, load_model_bundle, load_intents

BASE = Path(__file__).parent

with open(BASE / "health_advice.json", "r", encoding="utf-8") as f:
    HEALTH = json.load(f)

ensure_model()
MODEL, VECTORIZER, CLASSES = load_model_bundle()
INTENTS = load_intents()["intents"]

def predict_intent(message):
    X = VECTORIZER.transform([message]).toarray()
    probs = MODEL.predict(X, verbose=0)[0]
    idx = int(probs.argmax())
    return CLASSES[idx], float(probs[idx])

def symptom_check(message):
    text = message.lower()
    for symptom, info in HEALTH["symptoms"].items():
        if symptom in text:
            return {
                "type": "symptom",
                "triage": info["triage"],
                "advice": info["advice"],
                "red_flags": info["red_flags"],
            }
    return None

def reply_for_tag(tag):
    for intent in INTENTS:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I can help with basic health guidance, reminders, and wellness tips."

def generate_reply(message):
    low = message.lower()

    if any(x in low for x in ["suicidal", "self harm", "kill myself"]):
        return "This sounds urgent. Contact local emergency services or a trusted person right now and do not stay alone."

    symptom = symptom_check(message)
    if symptom:
        return {
            "reply": "Here is basic guidance based on your message.",
            "details": symptom,
        }

    tag, score = predict_intent(message)
    if score < 0.35:
        return {
            "reply": "I am not fully sure. Please describe your symptoms, duration, age, and any medicines you take.",
            "details": {"intent": tag, "confidence": score},
        }

    return {
        "reply": reply_for_tag(tag),
        "details": {"intent": tag, "confidence": score},
      }
