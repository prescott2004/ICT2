from flask import (
    request,
    redirect,
    url_for,
    render_template,
    flash,
    session,
    send_from_directory,
)
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group
from UC.models.chat import Chat
from werkzeug.utils import secure_filename
import os
import datetime


# URL: /にリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@app.route("/", methods=["GET", "POST"])
@is_logined
def show_home():
    group = Group.query.get(0)
    chats = Chat.query.filter(Chat.group_id == 0).order_by(Chat.time_post.desc()).all()
    # ホームに移動
    return render_template(
        "home/index.html", user=session["user"], group=group, chats=chats
    )
