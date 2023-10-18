from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("flask_blog.config")

# 他のプログラムはdbという変数を参照することでデータベースを扱えるようになった
db = SQLAlchemy(app)

from flask_blog.views import views, entries
