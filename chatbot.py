import requests
import json
import os

# ✅ Better chat-style model
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {
    "Authorization": "Bearer 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"  # 🔐 Replace safely
}

MEMORY_FILE = "bacchu_memory.json"

# 🧠 Load memory if it exists
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

# 🧠 Save memory
def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# 🧠 Optional: inject Bacchu’s character
persona = """
You're Bacchu. The user's old close friend – emotional, fun, dramatic, and supportive.
Speak casually in Hinglish, Marathi, or English based on how the user talks.
Don't call yourself a bestie or assistant. Just be YOU – a chill, heart-to-heart buddy.
"""

# 🧱 Build prompt with recent history + persona
def build_prompt(user_input):
    recent_history = ""
    for turn in history[-6:]:
        role = "User" if turn["role"] == "user" else "Bot"
        recent_history += f"{role}: {turn['content']}\n"

    return f"""{persona.strip()}

{recent_history.strip()}
User: {user_input}
Bot:"""

# 🚀 Query the Hugging Face API
def query(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True,
            "return_full_text": False,
            "stop": ["User:", "Bot:"]
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    print(f"\n📦 Raw response from API: {result}")

    try:
        generated_text = result[0]["generated_text"]
        reply = generated_text.strip()
    except Exception as e:
        reply = f"⚠️ API Error: {result.get('error', str(e))}"

    return reply

# 💬 Main chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        save_memory()
        print("🧠 Bacchu's memory saved. See you soon!")
        break

    prompt = build_prompt(user_input)
    reply = query(prompt)

    # ➕ Save structured turns
    history.append({"role": "user", "content": user_input})
    history.append({"role": "bot", "content": reply})
    save_memory()

    print(f"Bacchu: {reply}")
