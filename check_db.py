"""
Quick database check script
"""
import sqlite3
import os

db_path = 'instance/prompts.db'

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("📊 Database Tables:")
for table in tables:
    print(f"   - {table[0]}")

# Check alembic_version
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'")
has_alembic = cursor.fetchone()

if has_alembic:
    cursor.execute("SELECT version_num FROM alembic_version")
    version = cursor.fetchone()
    if version:
        print(f"\n📌 Current revision: {version[0]}")
    else:
        print("\n⚠️  alembic_version table exists but is empty")
else:
    print("\n⚠️  No alembic_version table found")

# Check users table structure
cursor.execute("PRAGMA table_info(users)")
user_columns = cursor.fetchall()

print("\n👤 Users table columns:")
for col in user_columns:
    print(f"   - {col[1]} ({col[2]})")

conn.close()
