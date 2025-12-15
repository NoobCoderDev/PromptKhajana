import sys
import os

# Add your project directory to the Python path
path = '/home/PromptKhajana/promptkhajana'  # Replace 'yourusername' with your PythonAnywhere username
if path not in sys.path:
    sys.path.append(path)

from run import app

if __name__ == "__main__":
    app.run()
