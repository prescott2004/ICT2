from flask import request, redirect, url_for, render_template, flash, session
from flask import request, redirect, url_for, render_template, flash, session
from flask import current_app as app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from flask import Blueprint

entry = Blueprint("entry", __name__)


# URL: /にリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@entry.route("/")
@login_required
def show_entries():
    # index.htmlに移動
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("entries/index.html", entries=entries)


# 新規投稿ボタンを押したときの遷移先
@entry.route("/entries/new", methods=["GET"])
@login_required
def new_entry():
    return render_template("entries/new.html")


# 投稿内容を受信してデータベースに保存する処理
@entry.route("/entries", methods=["POST"])
@login_required
def add_entry():
    entry = Entry(title=request.form["title"], text=request.form["text"])
    db.session.add(entry)
    db.session.commit()
    flash("新しく記事が作成されました")
    return redirect(url_for("entry.show_entries"))


# クリックすると記事本文等詳細が表示される
@entry.route("/entries/<int:id>", methods=["GET"])
@login_required
def show_entry(id):
    entry = Entry.query.get(id)
    return render_template("entries/show.html", entry=entry)


# 編集ボタンをクリックしたら編集画面を返す
@entry.route("/entries/<int:id>/edit", methods=["GET"])
@login_required
def edit_entry(id):
    entry = Entry.query.get(id)
    return render_template("entries/edit.html", entry=entry)


# フォームに入力された編集内容を受け取りDBを更新
@entry.route("/entries/<int:id>/update", methods=["POST"])
@login_required
def update_entry(id):
    entry = Entry.query.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    db.session.merge(entry)
    db.session.commit()
    flash("記事が更新されました")
    return redirect(url_for("entry.show_entries"))


# 削除ボタンが押されたときに該当の記事を削除する処理
@entry.route("/entries/<int:id>/delete", methods=["POST"])
@login_required
def delete_entry(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash("投稿が削除されました")
    return redirect(url_for("entry.show_entries"))
