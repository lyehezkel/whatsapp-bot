from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Load lists from file
def load_lists():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save lists to file
def save_lists(lists):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lists, f, ensure_ascii=False)

# Shared list for all users
lists = load_lists()

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    global lists
    incoming_msg = request.values.get('Body', '').strip().replace('\u200f', '')
    from_number = request.values.get('From')

    resp = MessagingResponse()
    msg = resp.message()

    # Everyone works on the same list under "shared"
    if "shared" not in lists:
        lists["shared"] = []

    if "רשימה חדשה" in incoming_msg:
        lists["shared"] = []
        save_lists(lists)
        msg.body("✅ רשימה חדשה נוצרה (משותפת לכל המשתמשים).")
    elif "הוסף" in incoming_msg:
        item = incoming_msg.replace("הוסף", "").strip()
        if item:
            lists["shared"].append(item)
            save_lists(lists)
            msg.body(f"📌 '{item}' נוסף לרשימה המשותפת.")
        else:
            msg.body("🔺 לא ציינת פריט להוסיף.")
    elif "הצג רשימה" in incoming_msg:
        if lists["shared"]:
            list_text = "\n".join(f"{i+1}. {item}" for i, item in enumerate(lists["shared"]))
            msg.body("📝 הרשימה המשותפת:\n" + list_text)
        else:
            msg.body("📭 הרשימה המשותפת ריקה.")
    else:
        msg.body("השתמש ב:\n- 'רשימה חדשה'\n- 'הוסף <פריט>'\n- 'הצג רשימה'")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
