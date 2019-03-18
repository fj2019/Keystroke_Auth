from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
from app import views
