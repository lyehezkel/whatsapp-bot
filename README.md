# WhatsApp List Bot (Hebrew)

This is a simple Flask app that acts as a WhatsApp bot using Twilio's WhatsApp Sandbox.
It allows users to:
- Start a new list
- Add items to the list
- Display the list

## How to Deploy

1. Push this project to GitHub
2. Create an account on [Render.com](https://render.com/)
3. Create a new Web Service and connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Environment Variable: `PORT=5000`
5. Set the webhook URL in Twilio to `https://your-app-name.onrender.com/whatsapp`

Enjoy!
