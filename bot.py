from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
lists = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().replace('\u200f', '')
    from_number = request.values.get('From')

    if from_number not in lists:
        lists[from_number] = []

    resp = MessagingResponse()
    msg = resp.message()

    if "רשימה חדשה" in incoming_msg:
        lists[from_number] = []
        msg.body("✅ רשימה חדשה נוצרה.")
    elif "הוסף" in incoming_msg:
        item = incoming_msg.replace("הוסף", "").strip()
        if item:
            lists[from_number].append(item)
            msg.body(f"📌 '{item}' נוסף לרשימה.")
        else:
            msg.body("🔺 לא ציינת פריט להוסיף.")
    elif "הצג רשימה" in incoming_msg:
        if lists[from_number]:
            list_text = "\n".join(f"{i+1}. {item}" for i, item in enumerate(lists[from_number]))
            msg.body("📝 הרשימה שלך:\n" + list_text)
        else:
            msg.body("📭 הרשימה שלך ריקה.")
    else:
        msg.body("השתמש ב:\n- 'רשימה חדשה'\n- 'הוסף <פריט>'\n- 'הצג רשימה'")

    return str(resp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
