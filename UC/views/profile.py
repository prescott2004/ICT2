from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.user import User


# プロフィールを見る
@app.route("/profile/<int:user_id>")
@is_logined
def show_profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile/profile.html", user=user)
