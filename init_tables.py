import psycopg2

db = psycopg2.connect("postgresql://postgres.wddrfawegzirdrrgoqpv:Y7hPzbxymY2jDrzI@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres")
cursor = db.cursor()

admin_table = """
CREATE TABLE IF NOT EXISTS admin_username_pass (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
"""
cursor.execute(admin_table)

events_table = """
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    date DATE,
    category VARCHAR(255),
    organizer VARCHAR(255),
    status VARCHAR(50),
    description TEXT,
    image_path VARCHAR(255),
    registration_link TEXT,
    sheet_link TEXT
)
"""
cursor.execute(events_table)

event_regs_table = """
CREATE TABLE IF NOT EXISTS event_registrations (
    id SERIAL PRIMARY KEY,
    event_id INT,
    student_name VARCHAR(255),
    student_email VARCHAR(255),
    attended INT DEFAULT 0
)
"""
cursor.execute(event_regs_table)

cursor.execute("SELECT COUNT(*) FROM admin_username_pass")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO admin_username_pass (username, password) VALUES ('admin', 'admin123')")

db.commit()
print("All tables successfully migrated correctly to Supabase.")
