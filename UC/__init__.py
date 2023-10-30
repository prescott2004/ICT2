from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("UC.config")
db = SQLAlchemy(app)

from UC.views import views, home, chats
