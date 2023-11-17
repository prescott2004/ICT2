from flask import request, redirect, url_for, render_template, flash, session
from UC.views.views import is_logined
from functools import wraps
from UC import app, db
from UC.models.user import User
from UC.models.group import Group
from sqlalchemy import or_


@app.route("/search", methods=["GET", "POST"])
@is_logined
def search():
    search_query = ""
    search_type = "init"
    search_results = []
    if request.method == "POST":
        search_query = request.form["query"]
        # 検索語が空だったら
        if search_query == "":
            flash("キーワードを入力してください")
            return redirect(url_for("search"))
        search_type = request.form["type"]
        # グループを検索する場合
        if search_type == "group":
            search_results = Group.query.filter(
                or_(
                    Group.title.contains(search_query),
                    Group.description.contains(search_query),
                )
            ).all()
        # ユーザを検索する場合
        elif search_type == "user":
            search_results = User.query.filter(
                or_(
                    User.name_first.contains(search_query),
                    User.name_last.contains(search_query),
                )
            ).all()
    return render_template(
        "search/search.html",
        search_query=search_query,
        search_type=search_type,
        search_results=search_results,
    )
