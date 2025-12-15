import os
import logging
from flask import Flask
from flask_migrate import upgrade
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from app import db

logger = logging.getLogger(__name__)

def ensure_migrations_initialized(app: Flask, migrations_dir: str = 'migrations'):
    if not os.path.exists(os.path.join(migrations_dir, 'alembic.ini')):
        logger.info("Initializing migrations directory...")
        with app.app_context():
            try:
                from flask_migrate import init
                init(directory=migrations_dir)
                logger.info("✅ Migrations directory initialized")
                return True
            except Exception as e:
                logger.error(f"Failed to initialize migrations: {e}")
                return False
    return True

def auto_migrate(app: Flask, migrations_dir: str = 'migrations'):
    with app.app_context():
        try:
            if not ensure_migrations_initialized(app, migrations_dir):
                logger.warning("Skipping auto-migration due to initialization failure")
                return False
            
            versions_dir = os.path.join(migrations_dir, 'versions')
            
            if not os.path.exists(versions_dir):
                os.makedirs(versions_dir)
            
            alembic_cfg = Config(os.path.join(migrations_dir, 'alembic.ini'))
            alembic_cfg.set_main_option('script_location', migrations_dir)
            
            script = ScriptDirectory.from_config(alembic_cfg)
            
            with db.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_rev = context.get_current_revision()
                
                if current_rev is None:
                    from sqlalchemy import inspect
                    inspector = inspect(db.engine)
                    
                    if inspector.has_table('users'):
                        logger.info("Database has existing tables. Marking initial migration as applied...")
                        command.stamp(alembic_cfg, '001_initial')
                        logger.info("Initial migration marked as applied")
                        current_rev = '001_initial'
            
            logger.info("Applying pending migrations...")
            upgrade(directory=migrations_dir)
            logger.info("✅ Database migrations applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Auto-migration failed: {e}")
            logger.info("Attempting safe fallback migration...")
            return safe_fallback_migration(app)

def safe_fallback_migration(app: Flask):
    try:
        import sqlite3
        from app.models import User, OTP
        
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        
        if not db_uri.startswith('sqlite:///'):
            logger.error("Fallback migration only supports SQLite")
            return False
        
        db_path = db_uri.replace('sqlite:///', '')
        
        if not os.path.isabs(db_path):
            instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
            os.makedirs(instance_path, exist_ok=True)
            db_path = os.path.join(instance_path, db_path)
        
        if not os.path.exists(db_path):
            logger.info("Database doesn't exist. Creating tables...")
            db.create_all()
            logger.info("✅ Database tables created")
            return True
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [row[1] for row in cursor.fetchall()]
        
        if 'email_verified' not in user_columns:
            logger.info("Adding email_verified column...")
            cursor.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT 0")
            conn.commit()
            logger.info("✅ Added email_verified column")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='otps'")
        if not cursor.fetchone():
            logger.info("Creating otps table...")
            cursor.execute("""
                CREATE TABLE otps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(120) NOT NULL,
                    otp_hash VARCHAR(200) NOT NULL,
                    purpose VARCHAR(20) NOT NULL,
                    expires_at DATETIME NOT NULL,
                    attempts INTEGER DEFAULT 0,
                    is_used BOOLEAN DEFAULT 0,
                    created_at DATETIME
                )
            """)
            cursor.execute("CREATE INDEX ix_otps_email ON otps (email)")
            conn.commit()
            logger.info("✅ Created otps table")
        
        conn.close()
        logger.info("✅ Fallback migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Fallback migration failed: {e}")
        return False
