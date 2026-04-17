from admin_login import app, send_new_event_email

def send_test_email():
    with app.app_context():
        success = send_new_event_email(
            event_name="Test Event from Assistant",
            event_date="2026-03-25",
            event_description="This is an automated test email to verify the inline image attachment fix is working perfectly.",
            event_organizer="Assistant Testing",
            event_image="webdev.png",
            host_url="http://127.0.0.1:5000/"
        )
        if success:
            print("Successfully sent the trial email!")
        else:
            print("Failed to send the trial email. Check the application logs above.")

if __name__ == "__main__":
    send_test_email()
