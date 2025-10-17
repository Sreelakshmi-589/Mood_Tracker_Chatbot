import pandas as pd
from datetime import datetime
import random

# Create or load a CSV file to store mood logs
try:
    mood_data = pd.read_csv("mood_log.csv")
except FileNotFoundError:
    mood_data = pd.DataFrame(columns=["Date", "Mood", "Note"])

# Defining response templates
greetings = ["Hi there!", "Hello!", "Hey!", "Nice to see you!"]
positive_responses = ["That's awesome!", "Keep it up!", "Glad to hear that!"]
neutral_responses = ["Okay, I understand.", "Got it.", "Thanks for sharing."]
negative_responses = ["I’m sorry to hear that.", "That sounds tough.", "I'm here for you."]
negative_tips = [
    "Try taking a short walk or doing some light exercise.",
    "Reach out to a friend or family member.",
    "Practice deep breathing for a few minutes.",
    "Write down your thoughts in a journal.",
    "Listen to your favorite music or watch a comforting show."
]
neutral_tips = [
    "Remember, it's okay to have ups and downs.",
    "Take a moment to reflect on something you enjoy.",
    "Stay hydrated and take care of yourself."
]
positive_tips = [
    "Keep spreading positivity!",
    "Celebrate your good moments.",
    "Share your happiness with someone else today!"
]

# Function to record mood
def log_mood(mood, note=""):
    global mood_data
    new_entry = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M"), "Mood": mood, "Note": note}
    mood_data = pd.concat([mood_data, pd.DataFrame([new_entry])], ignore_index=True)
    mood_data.to_csv("mood_log.csv", index=False)

# Function to classify mood
def mood_category(user_input):
    user_input = user_input.lower()
    if any(word in user_input for word in ["happy", "good", "great", "excited", "awesome", "joy"]):
        return "positive"
    elif any(word in user_input for word in ["sad", "bad", "upset", "depressed", "angry", "tired", "exhausted", "cry"]):
        return "negative"
    else:
        return "neutral"

# Function to respond
def chatbot_response(user_input):
    if "history" in user_input.lower():
        if mood_data.empty:
            return "You don't have any mood logs yet."
        else:
            last_entries = mood_data.tail(5)
            return f"Here are your last {len(last_entries)} mood entries:\n{last_entries.to_string(index=False)}"

    mood_type = mood_category(user_input)
    if mood_type == "positive":
        response = random.choice(positive_responses)
        tip = random.choice(positive_tips)
        full_response = f"{response}\nSuggestion: {tip}"
    elif mood_type == "negative":
        response = random.choice(negative_responses)
        tip = random.choice(negative_tips)
        full_response = f"{response}\nSuggestion: {tip}"
    else:
        response = random.choice(neutral_responses)
        tip = random.choice(neutral_tips)
        full_response = f"{response}\nSuggestion: {tip}"

    log_mood(mood_type, user_input)
    return full_response

# Conversation loop
print(random.choice(greetings))
print("I'm your Mood Tracker Bot 🌤️How are you feeling today? (Type 'bye' to exit)")


while True:
    user_input = input("You: ")
    if "bye" in user_input.lower():
        print("Chatbot: Goodbye! Remember to take care of yourself 💛")
        break
    print("Chatbot:", chatbot_response(user_input))
