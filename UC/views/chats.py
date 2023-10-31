from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group
from UC.models.chat import Chat


# URL: /chatsにリクエストがあったときのルーティング処理
# 参加しているグループを表示
@app.route("/chats")
@is_logined
def show_groups():
    """修正箇所"""
    # 全グループを取得
    groups = Group.query.order_by(Group.id.desc()).all()
    # 参加しているチャットグループ一覧を表示
    return render_template("chats/groups.html", groups=groups)


# 特定のグループのチャット一覧を表示
@app.route("/chats/<int:id>")
@is_logined
def show_chats(id):
    group = Group.query.get(id)
    chats = Chat.query.filter(Chat.group == group)
    # チャット画面に移動
    return render_template("chats/chats.html", group=group, chats=chats)
