from flask import request, redirect, url_for, render_template, flash, session

from flask import current_app as app
from functools import wraps
from flask import Blueprint

view = Blueprint("view", __name__)


# ログインしているか否かの判定
def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("view.login"))
        return view(*args, **kwargs)

    return inner


# URL: /loginにリクエストがあったときのルーティング処理
# GET, POSTメソッド使用
@view.route("/login", methods=["GET", "POST"])
def login():
    error = None
    # POSTメソッドでリクエストがあったとき, usernameとpasswordをチェック
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            # 表示させたい結果をflashに保存し、クライアントに返せるよう変更
            flash("ユーザ名が異なります")
        elif request.form["password"] != app.config["PASSWORD"]:
            # 表示させたい結果をflashに保存し、クライアントに返せるよう変更
            flash("パスワードが異なります")
        else:
            session["logged_in"] = True
            flash("ログインしました")
            # ルーティング
            # return redirect("/")
            return redirect(url_for("entry.show_entries"))
    # login.htmlに移動
    return render_template("login.html")


# URL: /logoutにリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@view.route("/logout")
def logout():
    # セッション情報を削除
    session.pop("logged_in", None)
    flash("ログアウトしました")
    # ルーティング
    # return redirect("/")
    return redirect(url_for("entry.show_entries"))


@view.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for("view.login"))
