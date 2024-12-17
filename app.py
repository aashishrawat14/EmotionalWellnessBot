import os
from flask import Flask, request, jsonify
from datetime import datetime
import openai
import sqlite3
from textblob import TextBlob

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
def init_db():
    conn = sqlite3.connect('emotional_wellness.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mood_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        mood TEXT,
                        sentiment REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Analyze sentiment using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Save mood log to database
def save_mood(user_id, mood, sentiment):
    conn = sqlite3.connect('emotional_wellness.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO mood_logs (user_id, mood, sentiment) 
                      VALUES (?, ?, ?)''', (user_id, mood, sentiment))
    conn.commit()
    conn.close()

# Fetch mood history from database
def get_mood_history(user_id):
    conn = sqlite3.connect('emotional_wellness.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT mood, sentiment, timestamp FROM mood_logs 
                      WHERE user_id = ? ORDER BY timestamp DESC''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Generate response from ChatGPT
def generate_response(user_input):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"You are an empathetic wellness bot. Respond to this: {user_input}",
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sorry, I couldn't process your request: {str(e)}"

# Routes
@app.route('/log_mood', methods=['POST'])
def log_mood():
    data = request.json
    user_id = data.get('user_id')
    mood = data.get('mood')

    if not user_id or not mood:
        return jsonify({"error": "Missing user_id or mood"}), 400

    sentiment = analyze_sentiment(mood)
    save_mood(user_id, mood, sentiment)

    return jsonify({"message": "Mood logged successfully", "sentiment": sentiment})

@app.route('/mood_history', methods=['GET'])
def mood_history():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    history = get_mood_history(user_id)
    return jsonify({"mood_history": history})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    response = generate_response(user_input)
    return jsonify({"response": response})

@app.route('/guided_exercise', methods=['GET'])
def guided_exercise():
    exercises = [
        "Take 5 deep breaths, inhaling through your nose and exhaling through your mouth.",
        "Close your eyes and visualize a peaceful place for 2 minutes.",
        "Write down three things you are grateful for today.",
        "Stretch your arms and legs for a few minutes to release tension."
    ]
    return jsonify({"exercise": exercises})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
