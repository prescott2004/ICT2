from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group


# URL: /chatsにリクエストがあったときのルーティング処理
@app.route("/chats")
@is_logined
def show_chatgroups():
    """修正箇所"""
    # ひとまず全グループを取得
    groups = Group.query.all()
    # 参加しているチャットグループ一覧を表示
    return render_template("chats/index.html", user=session["user"], groups=groups)
