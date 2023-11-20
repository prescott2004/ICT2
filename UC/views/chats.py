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


# URL: /chatsにリクエストがあったときのルーティング処理
# 参加しているグループを表示
@app.route("/chats")
@is_logined
def show_groups():
    """修正箇所"""
    # 全グループを取得
    groups = Group.query.filter(Group.id != 0).all()
    print(groups)
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
@app.route("/chats/<int:group_id>/send/<int:user_id>", methods=["POST"])
@is_logined
def send_chat(user_id, group_id):
    # チャット作成時刻
    time_post = datetime.datetime.now()
    # フォルダ作成
    os.makedirs(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]), exist_ok=True)
    file = request.files["file"]
    # チャットが空の場合、送らない
    if file.filename == "" and request.form["text"] == "":
        flash("何か入力してください")
    else:
        file_name = secure_filename(file.filename)
        # ファイルが存在する場合
        if file.filename != "":
            file_path = os.path.join(
                os.getcwd(),
                app.config["UPLOAD_FOLDER"],
                f"{file_name}_{user_id}_{time_post.strftime('%Y%m%d%H%M%S')}",
            )
            file.save(file_path)
        # チャット作成
        chat = Chat(
            user_id=user_id,
            group_id=group_id,
            time_post=time_post,
            text=request.form["text"],
            file_name=file_name,
        )
        db.session.add(chat)
        db.session.commit()
    # ページ更新
    if group_id == 0:
        return redirect(url_for("show_home"))

    return redirect(url_for("show_chats", id=group_id))


# ファイルダウンロード
@app.route("/chats/<int:group_id>/download/<file_name>/<int:user_id>/<time_post_str>")
@is_logined
def download_file(file_name, user_id, group_id, time_post_str):
    directory_path = os.path.join(
        os.getcwd(),
        app.config["UPLOAD_FOLDER"],
    )
    file_path = f"{file_name}_{user_id}_{time_post_str}"
    return send_from_directory(
        directory_path,
        file_path,
        as_attachment=True,
        download_name=file_name,
    )
