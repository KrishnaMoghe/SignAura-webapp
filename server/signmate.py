from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime
import spacy
from difflib import get_close_matches
import re

# ───────────────────────────────────────────────────────
# CONFIG
GESTURES_CSV = 'gestures.csv'
USER_GESTURES_CSV = 'user_added_gestures.csv'

# ───────────────────────────────────────────────────────
# INIT
app = Flask(__name__)
CORS(app)  # Allow frontend (React) access
nlp = spacy.load("en_core_web_sm")

# ───────────────────────────────────────────────────────
# HELPERS

def load_gestures():
    """Load gestures from both base and user-added CSVs"""
    gestures = {}
    for file in [GESTURES_CSV, USER_GESTURES_CSV]:
        if os.path.exists(file):
            with open(file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    gestures[row["gesture"].lower()] = row["description"]
    return gestures

def add_user_gesture(gesture, description):
    """Append new user-taught gesture to CSV"""
    gesture = gesture.lower()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(USER_GESTURES_CSV)

    with open(USER_GESTURES_CSV, 'a', newline='') as csvfile:
        fieldnames = ['gesture', 'description', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'gesture': gesture,
            'description': description,
            'timestamp': timestamp
        })

def extract_gesture(user_input):
    """
    Tries to extract the actual gesture name from phrases like:
    - What is the gesture for hello?
    - How do I sign thank you?
    - Tell me the sign of absent
    """
    user_input = user_input.lower()

    # Common patterns
    patterns = [
        r"gesture for ([a-z\s]+)",
        r"sign for ([a-z\s]+)",
        r"sign of ([a-z\s]+)",
        r"gesture of ([a-z\s]+)",
        r"how do i sign ([a-z\s]+)",
        r"how to sign ([a-z\s]+)",
        r"show me ([a-z\s]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input)
        if match:
            return match.group(1).strip()

    # fallback: use spacy to get noun
    doc = nlp(user_input)
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            return token.text.lower()

    return None

def find_closest_gesture(gesture, gesture_list):
    """Use fuzzy matching to guess closest known gesture"""
    matches = get_close_matches(gesture, gesture_list, n=1, cutoff=0.7)
    return matches[0] if matches else None

def detect_intent(user_input):
    """Basic rule-based intent detection"""
    u = user_input.lower()
    if any(q in u for q in ["gesture", "sign", "how do i", "what is"]):
        return "ask"
    elif any(q in u for q in ["it's like", "i'll teach", "describe", "teach", "means"]):
        return "teach"
    elif any(q in u for q in ["hi", "hello", "hey"]):
        return "greet"
    return "unknown"

# ───────────────────────────────────────────────────────
# ROUTES

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input = data.get("message", "")
    gestures = load_gestures()
    gesture_list = list(gestures.keys())
    
    intent = detect_intent(user_input)

    if intent == "greet":
        return jsonify({"response": "Hello! 👋 Ask me about any sign, like 'What is the gesture for thank you?'"})

    elif intent == "ask":
        gesture = extract_gesture(user_input)
        if gesture in gestures:
            return jsonify({"response": gestures[gesture]})
        else:
            close = find_closest_gesture(gesture, gesture_list)
            if close:
                return jsonify({"response": f"Did you mean '{close}'? The gesture is:\n\n{gestures[close]}"})
            return jsonify({
                "response": f"I don't know the gesture for '{gesture}'. Do you know it?",
                "suggest_learning": True,
                "missing_gesture": gesture
            })

    elif intent == "teach":
        return jsonify({"response": "Sure! Tell me the gesture and how it's performed using the /teach endpoint."})

    else:
        return jsonify({"response": "I'm not sure I understood. Try asking me something like: 'What is the gesture for absent?'"})

@app.route('/teach', methods=['POST'])
def teach():
    data = request.json
    gesture = data.get("gesture", "").strip().lower()
    description = data.get("description", "").strip()
    confirm = data.get("confirm", False)

    gestures = load_gestures()
    if gesture in gestures:
        return jsonify({"response": f"I already know the gesture for '{gesture}'."})

    if not confirm:
        return jsonify({
            "response": f"Are you sure you want to teach me this: '{gesture}' = '{description}'?",
            "confirm_needed": True
        })

    add_user_gesture(gesture, description)
    return jsonify({"response": f"Thanks! I've learned the gesture for '{gesture}'."})

# ───────────────────────────────────────────────────────
# START
if __name__ == '__main__':
    app.run(port=5001, debug=True)
