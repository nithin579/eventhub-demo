import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_cors import CORS
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app) # Allow cross-origin requests

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

url: str = "https://wddrfawegzirdrrgoqpv.supabase.co"
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route("/")
def home():
    return "EventHub Backend Running"

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
        
    try:
        supabase.table("subscribers").insert({"name": name, "email": email}).execute()
        return jsonify({"success": True, "message": "Successfully subscribed to notifications!"})
    except Exception as e:
        err = str(e).lower()
        if "duplicate" in err or "unique" in err:
            return jsonify({"error": "This email is already subscribed."}), 400
        print(f"Database error: {e}")
        return jsonify({"error": "An error occurred while subscribing."}), 500

@app.route("/add-event", methods=["POST", "OPTIONS"])
def add_event():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    data = request.json
    try:
        supabase.table("events").insert(data).execute()
        return jsonify({"success": True, "message": "Event created"})
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "An error occurred while adding event."}), 500

@app.route("/test")
def test_route():
    return jsonify({"success": True, "message": "Backend and Supabase are successfully connected with the Secret Key!"})

@app.route('/get-events')
def get_events():
    response = supabase.table('events').select("*").execute()
    return jsonify(response.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
