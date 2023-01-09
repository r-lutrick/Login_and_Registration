import re
from flask import Flask
app = Flask(__name__)
app.secret_key = "No secrets here..."

# Global Variables
DATABASE = "login_registration_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'[A-Z0-9]+')
