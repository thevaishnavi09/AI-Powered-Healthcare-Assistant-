# AI-Powered-Healthcare-Assistant-
Created a smart Al assistant to help people with their health questions and needs.Made it check symptoms, suggest basic advice, remind about medicines,&amp; offer simple mental health tips.Used Python and Al tools(Tensor Flow) to make it understand what people say and reply smartly.Kept everything organized using a database to store information safely.
# AI Powered Healthcare Assistant

A Flask + TensorFlow + SQLite healthcare assistant that can:
- check symptoms with simple rule-based guidance,
- suggest general self-care advice,
- send medication reminders,
- provide basic mental health tips,
- store chat/reminder data in SQLite.

> **Important:** This project is for educational purposes only and is not a medical diagnosis tool.

## Features
- Symptom checker with urgency levels.
- Intent classification with TensorFlow/Keras.
- Medication reminder CRUD.
- Mental health support responses.
- Conversation and reminder storage in SQLite.
- Clean web UI and REST API.

## Tech Stack
- Python 3.10+
- Flask
- TensorFlow / Keras
- SQLite
- HTML, CSS, JavaScript

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Train the model:
```bash
python train_model.py
```
4. Start the app:
```bash
python app.py
```
5. Open the browser at:
```bash
http://127.0.0.1:5000
```

## API
- `POST /api/chat`
- `POST /api/reminders`
- `GET /api/reminders/<user_id>`

## Safety Note
This assistant must not be used for emergencies. For chest pain, severe breathing trouble, stroke symptoms, suicidal thoughts, or other urgent issues, contact local emergency services immediately.
