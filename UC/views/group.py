from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group
from UC.models.chat import Chat


# URL: /chatsにリクエストがあったときのルーティング処理
# 参加しているグループを表示
@app.route("/create_group", methods=["GET", "POST"])
@is_logined
def create_group():
    # 参加しているチャットグループ一覧を表示
    # ログインしていたらホームに遷移
    # POSTメソッドでリクエストがあったとき, ユーザ登録
    if request.method == "POST":
        # グループ名が空だったら
        if request.form["group_name"] == "":
            flash("グループ名を入力してください")
            return redirect(url_for("create_group"))
        group = (
            db.session.query(Group)
            .filter(
                Group.title == request.form["group_name"],
            )
            .first()
        )
        # デバッグ用
        # print(f"登録ユーザ: {user}")
        # グループが登録されていない場合
        if group is None:
            group = Group(
                user_id_host=session["user"]["id"],
                title=request.form["group_name"],
                description=request.form["group_description"],
            )
            db.session.add(group)
            db.session.commit()
            # ログインページに移動
            flash("グループが登録されました")
            return redirect(url_for("show_groups"))
    # POSTメソッド以外の場合、ユーザ登録ページに移動
    return render_template("create_group.html")
