from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app,db
from flask_blog.models.entries import Entry


# URL: /にリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@app.route("/")
def show_entries():
    # ログインしているか否かの判別
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    # index.htmlに移動
    return render_template("entries/index.html")

# 新規投稿ボタンを押したときの遷移先
@app.route("/entries/new",methods=["GET"])
def new_entry():
    if not session.get("logged_in")
        return redirect(url_for("login"))
    return render_template("entries/new.html")


# 投稿内容を受信してデータベースに保存する処理