from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined


# URL: /にリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@app.route("/", methods=["GET"])
@is_logined
def show_home():
    # ホームに移動
    return render_template("home/index.html", user=session["user"])


# URL: /newにリクエストがあったときのルーティング処理
# 新規グループ作成
@app.route("/new", methods=["GET", "POST"])
@is_logined
def new_group():
    return render_template("/home/create_group.html", user=session["user"])
