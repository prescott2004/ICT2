from flask import request, redirect, url_for, render_template, flash, session
from functools import wraps
from UC import app, db
from UC.models.user import User
from UC.models.group import Group


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
            # 必要な情報が入力されていない場合
            if (
                request.form["name_last"] == ""
                or request.form["name_first"] == ""
                or request.form["email"] == ""
                or request.form["password"] == ""
            ):
                flash("必要な情報を入力してください")
            # 再入力パスワードが正しくない場合
            elif request.form["password"] != request.form["repassword"]:
                flash("パスワードが再入力と一致しません。")
            else:
                user = User(
                    name_last=request.form["name_last"],
                    name_first=request.form["name_first"],
                    email=request.form["email"],
                    password=request.form["password"],
                    user_type = request.form["user_type"],
                    description=request.form["description"],
                    affiliation=request.form["affiliation"]
                )
                if user.description=="":
                    user.description=" not entered "
                if user.affiliation=="":
                    user.affiliation="SECRET"
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
            if user.user_type == "company": session["company"]=True
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
    session.pop("company", None)
    flash("ログアウトしました")
    # ログインページに移動
    return redirect(url_for("login"))


@app.route("/option")
def option():
    return render_template("option.html")
    # セッションからユーザ名などを取得
    #
