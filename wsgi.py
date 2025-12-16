import sys
import os

# Add your project directory to the Python path
path = '/home/PromptKhajana/promptkhajana'
if path not in sys.path:
    sys.path.append(path)

# Import Flask app
from run import app

if __name__ == "__main__":
    app.run()
