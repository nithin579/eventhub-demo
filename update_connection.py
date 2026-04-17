import os

files = ["admin_login.py", "app.py", "init_tables.py"]
old_str = "postgresql://postgres:Y7hPzbxymY2jDrzI@db.wddrfawegzirdrrgoqpv.supabase.co:5432/postgres"
new_str = "postgresql://postgres.wddrfawegzirdrrgoqpv:Y7hPzbxymY2jDrzI@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_str, new_str)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print("Updated connection strings.")
