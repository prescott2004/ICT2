from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group
from UC.models.chat import Chat


# URL: /chatsにリクエストがあったときのルーティング処理
# 参加しているグループを表示
@app.route("/create_group",methods=["GET", "POST"])
@is_logined
def create_group():
    # 参加しているチャットグループ一覧を表示
        # ログインしていたらホームに遷移
    if session.get("logged_in"):
        return redirect(url_for("show_home"))
    # POSTメソッドでリクエストがあったとき, ユーザ登録
    if request.method == "POST":
        group = (
            db.session.query(Group)
            .filter(
                Group.title == request.form["title"],
            )
            .first()
        )
        # デバッグ用
        #print(f"登録ユーザ: {user}")
        # ユーザが登録されていない場合
        if user is None:
            user = Group(
                title=request.form["title"]
            )
            db.session.add(group)
            db.session.commit()
            # ログインページに移動
            flash("グループが登録されました")
            return redirect(url_for("create_group"))
    # POSTメソッド以外の場合、ユーザ登録ページに移動
    return render_template("create_group.html")