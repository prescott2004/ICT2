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
    groups = Group.query.all()
    # 参加しているチャットグループ一覧を表示
    return render_template("chats/groups.html", groups=groups)


# 特定のグループのチャット一覧を表示
@app.route("/chats/<int:id>")
@is_logined
def show_chats(id):
    group = Group.query.get(id)
    chats = (
        Chat.query.filter(Chat.group_id == group.id)
        .order_by(Chat.time_post.asc())
        .all()
    )
    # チャット画面に移動
    return render_template(
        "chats/chats.html", user=session["user"], group=group, chats=chats
    )


# チャット送信
@app.route("/chats/send/<int:user_id>/<int:group_id>", methods=["POST"])
@is_logined
def send_chat(user_id, group_id):
    # チャット作成
    chat = Chat(user_id=user_id, group_id=group_id, text=request.form["text"])
    db.session.add(chat)
    db.session.commit()
    # ページ更新
    return redirect(url_for("show_chats", id=group_id))
