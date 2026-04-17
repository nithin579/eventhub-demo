import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from supabase import create_client, Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import requests
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ===== Email Configuration =====
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

url: str = "https://wddrfawegzirdrrgoqpv.supabase.co"
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_sheet_id(sheet_url):
    if not sheet_url:
        return None
    try:
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error extracting sheet ID: {e}")
        return None

def send_new_event_email(event_name, event_date, event_description, event_organizer, event_image=None, host_url=None):
    with app.app_context():
        try:
            response = supabase.table("subscribers").select("email, name").eq("status", "active").execute()
            subscribers = response.data
            
            if not subscribers:
                return True
                
            recipients = [sub['email'] for sub in subscribers]
            
            msg = Message(
                subject=f"New Event Created: {event_name}!",
                sender=app.config.get("MAIL_USERNAME"),
                bcc=recipients
            )
            if event_image:
                try:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], event_image)
                    with open(file_path, 'rb') as fp:
                        ext = event_image.rsplit('.', 1)[1].lower() if '.' in event_image else 'jpeg'
                        content_type = f"image/{ext}"
                        if ext == 'jpg': content_type = "image/jpeg"
                        msg.attach(filename=event_image, content_type=content_type, data=fp.read(), disposition='inline', headers={'Content-ID': '<event_img>'})
                    image_html = '<br><img src="cid:event_img" alt="Event Image" style="max-width: 600px;"><br>'
                except Exception as e:
                    print(f"Error attaching image: {e}")
                    image_html = f'<br><img src="{host_url}static/uploads/{event_image}" alt="Event Image" style="max-width: 600px;"><br>' if host_url else ""
            else:
                image_html = ""
            
            msg.html = f"""
            <h2>New Event: {event_name}</h2>
            <p><strong>Date:</strong> {event_date}</p>
            <p><strong>Organizer:</strong> {event_organizer}</p>
            <p>{event_description}</p>
            {image_html}
            <br>
            <p>Visit the EventHub website to learn more and register!</p>
            """
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email notifications: {e}")
            return False

# ===== Public Routes =====
@app.route("/")
def home():
    return render_template("index.html")

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
        return jsonify({"error": "An error occurred while subscribing."}), 500

@app.route("/event-details.html")
def event_details():
    return render_template("event-details.html")

# ===== Admin Authentication Routes =====
@app.route("/admin")
def admin_login_page():
    session.pop("admin", None)
    return render_template("admin_login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if not username or not password:
        flash("Username and password are required")
        return redirect(url_for("admin_login_page"))
    try:
        res = supabase.table("admin_username_pass").select("*").eq("username", username).eq("password", password).execute()
        admin = res.data
        if admin and len(admin) > 0:
            session["admin"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Password")
            return redirect(url_for("admin_login_page"))
    except Exception as e:
        print(f"API error during login: {e}")
        flash("An error occurred during login. Please try again.")
        return redirect(url_for("admin_login_page"))

@app.route("/dashboard")
def dashboard():
    if "admin" in session:
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for("admin_login_page"))

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login_page"))

# ===== API Event Routes =====
@app.route("/api/events", methods=["GET"])
def get_events():
    try:
        res = supabase.table("events").select("*").order("id", desc=True).execute()
        events = res.data
        return jsonify(events)
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/events", methods=["POST"])
def create_event():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        name = request.form.get("name")
        date = request.form.get("date")
        category = request.form.get("category")
        organizer = request.form.get("organizer")
        status = request.form.get("status")
        description = request.form.get("description", "")
        registration_link = request.form.get("registration_link", "")
        sheet_link = request.form.get("responses_sheet_link", "")
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = filename

        payload = {
            "name": name, "date": date, "category": category, "organizer": organizer,
            "status": status, "description": description, "image_path": image_path,
            "registration_link": registration_link, "sheet_link": sheet_link
        }
        res = supabase.table("events").insert(payload).execute()
        new_id = res.data[0]['id'] if res.data else None
        
        try:
            send_new_event_email(name, date, description, organizer, image_path, request.host_url)
        except Exception as email_err:
            print(f"Failed to send email updates: {email_err}")
        
        return jsonify({"success": True, "message": "Event created", "id": new_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/events/<int:id>", methods=["PUT"])
def update_event(id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        name = request.form.get("name")
        date = request.form.get("date")
        category = request.form.get("category")
        organizer = request.form.get("organizer")
        status = request.form.get("status")
        description = request.form.get("description", "")
        registration_link = request.form.get("registration_link", "")
        sheet_link = request.form.get("responses_sheet_link", "")
        
        res = supabase.table("events").select("image_path").eq("id", id).execute()
        current_event = res.data[0] if res.data else None
        if not current_event:
             return jsonify({"error": "Event not found"}), 404
             
        image_path = current_event.get('image_path')
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = filename

        payload = {
            "name": name, "date": date, "category": category, "organizer": organizer,
            "status": status, "description": description, "image_path": image_path,
            "registration_link": registration_link, "sheet_link": sheet_link
        }
        supabase.table("events").update(payload).eq("id", id).execute()
        return jsonify({"success": True, "message": "Event updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        res = supabase.table("events").delete().eq("id", id).execute()
        if len(res.data) > 0:
            return jsonify({"success": True, "message": "Event deleted"})
        else:
            return jsonify({"error": "Event not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== API Student Routes =====
@app.route("/api/events/<int:event_id>/students", methods=["GET"])
def get_students(event_id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        res = supabase.table("event_registrations").select("*").eq("event_id", event_id).order("id", desc=True).execute()
        return jsonify(res.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/events/<int:event_id>/sync_students", methods=["POST"])
def sync_students(event_id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        res = supabase.table("events").select("sheet_link").eq("id", event_id).execute()
        event = res.data[0] if res.data else None
        if not event or not event.get('sheet_link'):
            return jsonify({"error": "No Google Sheet responses link is configured for this event. Please edit the event and provide the Responses Spreadsheet Link."}), 400
            
        sheet_id = extract_sheet_id(event['sheet_link'])
        if not sheet_id:
            return jsonify({"error": "Invalid Google Sheet link. Could not extract spreadsheet ID."}), 400
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_path = os.path.join(app.root_path, "credentials.json")
        if not os.path.exists(creds_path):
             return jsonify({"error": "Server is missing Google Sheets credentials."}), 500
             
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        try:
            sheet = client.open_by_key(sheet_id).sheet1
            rows = sheet.get_all_records()
        except Exception as sheet_err:
            return jsonify({"error": f"Failed to open Google Sheet. Make sure the link is correct and the service account has 'Viewer' access. Details: {sheet_err}"}), 400

        if not rows:
             return jsonify({"success": True, "message": "Sheet is empty, no students synced.", "added": 0})
             
        headers = list(rows[0].keys())
        name_col = next((h for h in headers if "name" in str(h).lower()), None)
        email_col = next((h for h in headers if "email" in str(h).lower() or "mail" in str(h).lower()), None)
        if not name_col or not email_col:
             return jsonify({"error": "Could not auto-detect Name and Email columns in the spreadsheet. Please ensure headers contain 'Name' and 'Email'."}), 400

        reg_res = supabase.table("event_registrations").select("student_email").eq("event_id", event_id).execute()
        existing_emails = {r['student_email'].strip().lower() for r in reg_res.data}
        
        to_insert = []
        for row in rows:
            student_name = str(row.get(name_col, "")).strip()
            student_email = str(row.get(email_col, "")).strip()
            if not student_name or not student_email: continue
            email_lower = student_email.lower()
            if email_lower not in existing_emails:
                to_insert.append({"event_id": event_id, "student_name": student_name, "student_email": student_email})
                existing_emails.add(email_lower)
                
        if to_insert:
            supabase.table("event_registrations").insert(to_insert).execute()
        return jsonify({"success": True, "message": f"Successfully synced {len(to_insert)} new students!", "added": len(to_insert)})
        
    except Exception as ex:
        print(f"Server error: {ex}")
        return jsonify({"error": str(ex)}), 500

@app.route("/api/events/<int:event_id>/students", methods=["POST"])
def add_student(event_id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
            
        payload = {"event_id": event_id, "student_name": name, "student_email": email}
        res = supabase.table("event_registrations").insert(payload).execute()
        new_id = res.data[0]['id'] if res.data else None
        return jsonify({"success": True, "message": "Student added", "id": new_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/students/batch_attendance", methods=["PUT"])
def batch_update_attendance():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        updates = data.get("updates", [])
        if not updates:
            return jsonify({"success": True, "message": "No updates provided"})

        # Using upsert to batch update items based on their primary key.
        supabase.table("event_registrations").upsert(updates).execute()
        
        return jsonify({"success": True, "message": f"Successfully updated {len(updates)} records"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        supabase.table("event_registrations").delete().eq("id", student_id).execute()
        return jsonify({"success": True, "message": "Student removed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== API Reports Routes =====
@app.route("/api/reports", methods=["GET"])
def get_reports():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        # Fetch events along with their registrations to compute aggregates programmatically
        res = supabase.table("events").select("id, name, category, date, event_registrations(id, attended)").execute()
        events_data = res.data
        
        reports = []
        for e in events_data:
            regs = e.get("event_registrations", [])
            total_reg = len(regs) if type(regs) == list else 0
            # attended is sometimes stored as int (1/0) or boolean depending on db engine types. Convert properly.
            total_att = sum(1 for r in regs if r.get('attended') in [1, True, "1"]) if type(regs) == list else 0
            
            reports.append({
                "id": e['id'],
                "name": e['name'],
                "category": e['category'],
                "date": e['date'],
                "total_registered": total_reg,
                "total_attended": total_att
            })
            
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== Settings API =====
@app.route("/api/settings/credentials", methods=["PUT"])
def update_credentials():
    if "admin" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        new_username = data.get("new_username", "").strip()
        new_password = data.get("new_password", "").strip()
        if not new_password:
            return jsonify({"error": "New password is required"}), 400
            
        current_username = session["admin"]
        
        if new_username:
            if new_username != current_username:
                res = supabase.table("admin_username_pass").select("id").eq("username", new_username).execute()
                if res.data and len(res.data) > 0:
                    return jsonify({"error": "Username already taken"}), 400
            supabase.table("admin_username_pass").update({"username": new_username, "password": new_password}).eq("username", current_username).execute()
            session["admin"] = new_username
        else:
            supabase.table("admin_username_pass").update({"password": new_password}).eq("username", current_username).execute()
            
        return jsonify({"success": True, "message": "Credentials updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test")
def test_route():
    return jsonify({"success": True, "message": "Backend and Supabase are successfully connected with the Secret Key!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
