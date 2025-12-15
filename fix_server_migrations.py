#!/usr/bin/env python3
"""
Fix Server Migrations Script
=============================
This script resolves the "Can't locate revision identified by '001_initial'" error
on the PythonAnywhere server by properly stamping the database with the current migration state.

Usage:
    python fix_server_migrations.py

What it does:
1. Checks if migrations directory exists
2. Verifies database tables exist
3. Stamps the database with the correct revision
4. Validates the migration state
"""

import os
import sys
from flask import Flask
from flask_migrate import stamp
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import inspect

def create_app():
    """Create minimal Flask app for migration operations"""
    from app import create_app
    return create_app()

def check_migrations_exist():
    """Check if migrations directory and files exist"""
    migrations_dir = 'migrations'
    
    if not os.path.exists(migrations_dir):
        print("❌ ERROR: migrations directory not found!")
        print("   Run: flask db init")
        return False
    
    versions_dir = os.path.join(migrations_dir, 'versions')
    if not os.path.exists(versions_dir):
        print("❌ ERROR: migrations/versions directory not found!")
        return False
    
    initial_migration = os.path.join(versions_dir, '001_initial.py')
    if not os.path.exists(initial_migration):
        print("❌ ERROR: 001_initial.py migration file not found!")
        return False
    
    print("✅ Migration files exist")
    return True

def check_database_tables(app):
    """Check if database tables already exist"""
    from app import db
    
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        required_tables = ['users', 'categories', 'tags', 'prompts', 'prompt_tags', 'otps']
        existing_tables = [t for t in required_tables if t in tables]
        
        print(f"\n📊 Database Status:")
        print(f"   Total tables: {len(tables)}")
        print(f"   Required tables found: {len(existing_tables)}/{len(required_tables)}")
        
        for table in required_tables:
            status = "✅" if table in tables else "❌"
            print(f"   {status} {table}")
        
        return len(existing_tables) == len(required_tables)

def get_current_revision(app):
    """Get the current database revision"""
    from app import db
    
    with app.app_context():
        alembic_cfg = Config('migrations/alembic.ini')
        alembic_cfg.set_main_option('script_location', 'migrations')
        
        with db.engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_rev = context.get_current_revision()
            
            if current_rev:
                print(f"\n📌 Current database revision: {current_rev}")
            else:
                print("\n⚠️  Database has no revision stamp (alembic_version table empty or missing)")
            
            return current_rev

def stamp_database(app, revision='001_initial'):
    """Stamp the database with the specified revision"""
    from app import db
    import sqlite3
    
    print(f"\n🔨 Stamping database with revision: {revision}")
    
    with app.app_context():
        try:
            alembic_cfg = Config('migrations/alembic.ini')
            alembic_cfg.set_main_option('script_location', 'migrations')
            
            # Try using alembic command first
            try:
                command.stamp(alembic_cfg, revision)
                print(f"✅ Database stamped successfully with revision: {revision}")
                return True
            except Exception as stamp_error:
                print(f"⚠️  Alembic stamp failed: {stamp_error}")
                print("   Attempting direct database update...")
                
                # Fallback: Direct database update for SQLite
                db_uri = app.config['SQLALCHEMY_DATABASE_URI']
                if db_uri.startswith('sqlite:///'):
                    db_path = db_uri.replace('sqlite:///', '')
                    if not os.path.isabs(db_path):
                        instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
                        db_path = os.path.join(instance_path, db_path)
                    
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Check if alembic_version table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'")
                    if cursor.fetchone():
                        # Update existing version
                        cursor.execute("UPDATE alembic_version SET version_num=?", (revision,))
                    else:
                        # Create table and insert version
                        cursor.execute("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)")
                        cursor.execute("INSERT INTO alembic_version VALUES (?)", (revision,))
                    
                    conn.commit()
                    conn.close()
                    print(f"✅ Database stamped successfully with revision: {revision} (direct update)")
                    return True
                else:
                    print("❌ Direct update only supported for SQLite")
                    return False
                    
        except Exception as e:
            print(f"❌ Failed to stamp database: {e}")
            return False

def verify_stamp(app):
    """Verify the stamp was applied correctly"""
    current_rev = get_current_revision(app)
    
    if current_rev == '001_initial':
        print("\n✅ Verification successful! Database is now at revision '001_initial'")
        return True
    else:
        print(f"\n❌ Verification failed! Expected '001_initial', got '{current_rev}'")
        return False

def main():
    """Main execution function"""
    print("=" * 70)
    print("🔧 Server Migration Fix Script")
    print("=" * 70)
    
    # Step 1: Check migrations exist
    print("\n[Step 1/5] Checking migration files...")
    if not check_migrations_exist():
        print("\n❌ Migration files are missing. Please ensure migrations are committed to git.")
        sys.exit(1)
    
    # Step 2: Create app
    print("\n[Step 2/5] Initializing Flask app...")
    try:
        app = create_app()
        print("✅ Flask app initialized")
    except Exception as e:
        print(f"❌ Failed to create app: {e}")
        sys.exit(1)
    
    # Step 3: Check database tables
    print("\n[Step 3/5] Checking database tables...")
    tables_exist = check_database_tables(app)
    
    # Step 4: Get current revision
    print("\n[Step 4/5] Checking current database revision...")
    current_rev = get_current_revision(app)
    
    # Step 5: Stamp if needed
    print("\n[Step 5/5] Applying fix...")
    
    if current_rev == '001_initial':
        print("✅ Database is already at the correct revision. No action needed!")
    elif current_rev is None and tables_exist:
        print("⚠️  Tables exist but no revision stamp found. Stamping database...")
        if stamp_database(app, '001_initial'):
            verify_stamp(app)
        else:
            sys.exit(1)
    elif current_rev is None and not tables_exist:
        print("⚠️  No tables and no revision. You should run: flask db upgrade")
        sys.exit(1)
    else:
        print(f"⚠️  Unexpected revision: {current_rev}")
        print("    Attempting to stamp with '001_initial'...")
        if stamp_database(app, '001_initial'):
            verify_stamp(app)
        else:
            sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ Migration fix completed successfully!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run: flask db upgrade")
    print("  2. Verify your application works correctly")
    print("=" * 70)

if __name__ == '__main__':
    main()
