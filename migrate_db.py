import os

def migrate_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Imports
    content = content.replace("import mysql.connector", "import psycopg2\nimport psycopg2.extras")
    content = content.replace("from mysql.connector import Error", "from psycopg2 import Error")
    
    # 2. Connection string
    old_conn = """db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root", 
            database="admin_login",
            auth_plugin='mysql_native_password'
        )"""
    new_conn = """db = psycopg2.connect("postgresql://postgres:Y7hPzbxymY2jDrzI@db.wddrfawegzirdrrgoqpv.supabase.co:5432/postgres")"""
    content = content.replace(old_conn, new_conn)
    
    old_conn_app = """db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "eventhub"),
            auth_plugin='mysql_native_password'
        )"""
    new_conn_app = """db = psycopg2.connect("postgresql://postgres:Y7hPzbxymY2jDrzI@db.wddrfawegzirdrrgoqpv.supabase.co:5432/postgres")"""
    content = content.replace(old_conn_app, new_conn_app)
    
    # 3. Connection property
    content = content.replace("db.is_connected()", "(not db.closed)")
    
    # 4. Cursor dictionary
    content = content.replace("cursor(dictionary=True)", "cursor(cursor_factory=psycopg2.extras.RealDictCursor)")
    
    # 5. Schema changes
    content = content.replace("id INT AUTO_INCREMENT PRIMARY KEY", "id SERIAL PRIMARY KEY")
    
    # 6. Exceptions
    content = content.replace("e.errno == 1062", "hasattr(e, 'pgcode') and e.pgcode == '23505'")
    
    # 7. Lastrowid (events logic)
    old_events_insert = """        query = \"\"\"
            INSERT INTO events (name, date, category, organizer, status, description, image_path, registration_link, sheet_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        \"\"\"
        cursor.execute(query, (name, date, category, organizer, status, description, image_path, registration_link, sheet_link))
        db.commit()
        new_id = cursor.lastrowid"""
        
    new_events_insert = """        query = \"\"\"
            INSERT INTO events (name, date, category, organizer, status, description, image_path, registration_link, sheet_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        \"\"\"
        cursor.execute(query, (name, date, category, organizer, status, description, image_path, registration_link, sheet_link))
        new_id = cursor.fetchone()[0]
        db.commit()"""
    content = content.replace(old_events_insert, new_events_insert)

    # Lastrowid (student logic)
    old_student_insert = """        query = "INSERT INTO event_registrations (event_id, student_name, student_email) VALUES (%s, %s, %s)"
        cursor.execute(query, (event_id, name, email))
        db.commit()
        return jsonify({"success": True, "message": "Student added", "id": cursor.lastrowid})"""

    new_student_insert = """        query = "INSERT INTO event_registrations (event_id, student_name, student_email) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (event_id, name, email))
        new_id = cursor.fetchone()[0]
        db.commit()
        return jsonify({"success": True, "message": "Student added", "id": new_id})"""
    content = content.replace(old_student_insert, new_student_insert)

    # psycopg2 needs fetchall instead of fetchmany for 'events' api to prevent unread query errors in later operations if cursor is reused without closing, but we close.
    # also boolean types in PG vs tinyint in MySQL for attended property, though psycopg2 will handle it fine.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

migrate_file("admin_login.py")
migrate_file("app.py")
print("Migration script executed successfully.")
