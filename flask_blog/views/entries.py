from flask import request, redirect, url_for, render_template, flash, session
from flask import request, redirect, url_for, render_template, flash, session
from flask_blog import app, db
from flask_blog.models.entries import Entry


# URL: /にリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@app.route("/")
def show_entries():
    # ログインしているか否かの判別
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    # index.htmlに移動
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("entries/index.html", entries=entries)


# 新規投稿ボタンを押したときの遷移先
@app.route("/entries/new", methods=["GET"])
def new_entry():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("entries/new.html")


# 投稿内容を受信してデータベースに保存する処理
@app.route("/entries", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    entry = Entry(title=request.form["title"], text=request.form["text"])
    db.session.add(entry)
    db.session.commit()
    flash("新しく記事が作成されました")
    return redirect(url_for("show_entries"))


# クリックすると記事本文等詳細が表示される
@app.route("/entries/<int:id>", methods=["GET"])
def show_entry(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    entry = Entry.query.get(id)
    return render_template("entries/show.html", entry=entry)


# 編集ボタンをクリックしたら編集画面を返す
@app.route("/entries/<int:id>/edit", methods=["GET"])
def edit_entry(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    entry = Entry.query.get(id)
    return render_template("entries/edit.html", entry=entry)


# フォームに入力された編集内容を受け取りDBを更新
@app.route("/entries/<int:id>/update", methods=["POST"])
def update_entry(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    entry = Entry.query.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    db.session.merge(entry)
    db.session.commit()
    flash("記事が更新されました")
    return redirect(url_for("show_entries"))
