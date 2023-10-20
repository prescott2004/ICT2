from flask import request, redirect, url_for, render_template, flash, session


from functools import wraps
from UC import app, db
from UC.models.user import User


# ログイン済みか判別
def is_logined(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return inner


# URL: /signupにリクエストがあったときのルーティング処理
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # ログインしていたらホームに遷移
    if session.get("logged_in"):
        return redirect(url_for("show_home"))
    # POSTメソッドでリクエストがあったとき, ユーザ登録
    if request.method == "POST":
        user = (
            db.session.query(User)
            .filter(
                User.email == request.form["email"],
            )
            .first()
        )
        # デバッグ用
        print(f"登録ユーザ: {user}")
        # ユーザが登録されていない場合
        if user is None:
            # 再入力パスワードが正しくない場合
            if request.form["password"] != request.form["repassword"]:
                flash("パスワードが再入力と一致しません。")
            else:
                user = User(
                    name_last=request.form["name_last"],
                    name_first=request.form["name_first"],
                    email=request.form["email"],
                    password=request.form["password"],
                )
                db.session.add(user)
                db.session.commit()
                # ログインページに移動
                flash("ユーザ登録されました")
                return redirect(url_for("login"))
        # ユーザが既に登録されている場合
        else:
            flash("登録済みのメールアドレスです!")
    # POSTメソッド以外の場合、ユーザ登録ページに移動
    return render_template("signup.html")


# URL: /loginにリクエストがあったときのルーティング処理
# GET, POSTメソッド使用
@app.route("/login", methods=["GET", "POST"])
def login():
    # ログインしていたらホームに遷移
    if session.get("logged_in"):
        return redirect(url_for("show_home"))

    # POSTメソッドでリクエストがあったとき, usernameとpasswordをチェック
    if request.method == "POST":
        user = (
            db.session.query(User)
            .filter(
                User.email == request.form["email"],
                User.password == request.form["password"],
            )
            .first()
        )
        # デバッグ用
        print(f"ログインユーザ: {user}")
        # ユーザが見つからなかった場合
        if user is None:
            flash("メールアドレスかパスワードが異なります")
        # ユーザが見つかった場合
        else:
            print(type(user.__dict__))
            # セッション情報を保存
            session["logged_in"] = True
            session["user"] = user.as_dict()
            flash("ログインしました")
            # ホームに移動
            return redirect(url_for("show_home"))
    # POSTメソッド以外の場合、ログインページに移動
    return render_template("login.html")


# URL: /logoutにリクエストがあったときのルーティング処理
# GETメソッド使用（デフォルト）
@app.route("/logout")
def logout():
    # セッション情報を削除
    session.pop("logged_in", None)
    session.pop("user", None)
    flash("ログアウトしました")
    # ログインページに移動
    return redirect(url_for("login"))
