from flask import Flask
from app import views

app = Flask(__name__)# type:Flask
app.config.from_object('config')
