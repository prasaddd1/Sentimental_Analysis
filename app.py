import os
import sqlite3
import requests
from datetime import datetime

# Initialize database
def create_database():
    conn = sqlite3.connect("sentiment_analysis.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()  # Ensure changes are saved
    conn.close()   # Close the connection

# Log result in the database
def log_result(input_text, sentiment):
    try:
        conn = sqlite3.connect("sentiment_analysis.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sentiment_analysis (input_text, sentiment, timestamp)
            VALUES (?, ?, ?)
        """, (input_text, sentiment, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database Error: {e}")
    finally:
        conn.close() 

# Analyze sentiment using OpenAI API
def analyze_sentiment(input_text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: API key not found."

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"Analyze the sentiment: {input_text}"}]
        }
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error: {response.text}"

# Main function
def main():
    create_database()
    input_text = input("Enter text to analyze sentiment: ")
    sentiment = analyze_sentiment(input_text)
    print(f"\nSentiment: {sentiment}")
    log_result(input_text, sentiment)

if __name__ == "__main__":
    main()
