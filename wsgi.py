import sys
import os

# ============================================================================
# ENVIRONMENT VARIABLES (Required for PythonAnywhere Free Plan)
# ============================================================================
# PythonAnywhere free plan doesn't support .env files or dashboard env vars
# Set all environment variables here BEFORE importing the app
# ============================================================================

# Flask Configuration
os.environ['SECRET_KEY'] = 'your-secret-key-here-change-this-to-random-string'

# Database Configuration (SQLite by default)
# os.environ['DATABASE_URL'] = 'sqlite:///prompts.db'  # Default, can be omitted

# Email Configuration (Gmail SMTP)
os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
os.environ['MAIL_PORT'] = '587'
os.environ['MAIL_USE_TLS'] = 'True'
os.environ['MAIL_USE_SSL'] = 'False'
os.environ['MAIL_USERNAME'] = 'prompt.khajana@gmail.com'  
os.environ['MAIL_PASSWORD'] = 'jqod aryv hwpj kdyy' 
os.environ['MAIL_DEFAULT_SENDER'] = 'prompt.khajana@gmail.com'

# Add your project directory to the Python path
path = '/home/PromptKhajana/promptkhajana'
if path not in sys.path:
    sys.path.append(path)

# Import Flask app
from run import app

if __name__ == "__main__":
    app.run()
