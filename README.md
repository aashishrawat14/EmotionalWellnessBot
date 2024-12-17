# Emotional Wellness Bot

This is a Flask-based emotional wellness bot that helps users log their mood, receive empathetic responses, and perform guided exercises.

## Features
1. Log moods and analyze sentiment.
2. Retrieve mood history.
3. Chat with an empathetic bot.
4. Get guided exercises for emotional wellness.

## Setup
1. Install Python 3.9+ and pip.
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key to the `.env` file.
4. Run the app:
   ```
   python app.py
   ```
5. Access the API at `http://127.0.0.1:5000`.

## API Endpoints
- `POST /log_mood`: Log a user's mood.
- `GET /mood_history`: Retrieve a user's mood history.
- `POST /chat`: Chat with the bot.
- `GET /guided_exercise`: Get a guided exercise.

## Notes
- Ensure the `emotional_wellness.db` SQLite database is in the project directory.
