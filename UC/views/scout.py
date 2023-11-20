from flask import request, redirect, url_for, render_template, flash, session
from UC import app, db
from UC.views.views import is_logined
from UC.models.group import Group
from UC.models.user import User
from UC.models.scout import Scout


# URL: /scoutにリクエストがあったときのルーティング処理
# スカウト学生の検索 [学生アカウント一覧を表示--修正したいかも？？]
 #・学生アカウントのプロフィールの表示　機能
 #・スカウト確認機能
 #・可能スカウト回数のデクリメント
@app.route("/scout")
@is_logined
def search_students():
    # 全学生ユーザを取得
    students = User.query.filter(User.user_type == "student")
    #students = User.query.all()
    user = session["user"]['id']
    #user = user['id']
    # 全学生の内，スカウト済みの学生を省く
    #students = students.filter(Scout.company_id==user, Scout.result=="")
    # 学生ユーザ一覧を表示
    return render_template("scout/scout_search.html", students=students, Scout=Scout)


# スカウト中の学生一覧の表示
@app.route("/scout/<int:user_id>")
@is_logined
def show_scout(user_id):
    scout = Scout.query.filter(Scout.company_id == user_id)
    return render_template(
        "scout/scout_list.html", user=session["user"], scouts = scout
    )

# スカウト実行
@app.route("/scout/<int:company_id>/<int:student_id>")
@is_logined
def student_scout(company_id,student_id):
    # ユーザ企業のid+名前と、スカウトされた学生のid+名前の確認
    user = session["user"]
    company_id = user['id']
    company_name = user['name_last'] + " " + user['name_first']
    student = User.query.filter_by(id=student_id).first()
    student_name = student.name_last + " " + student.name_first
    # Scoutデータベース・テーブルに記録
    scout = Scout(company_id=company_id, student_id=student_id, company_name=company_name, student_name=student_name)
    db.session.add(scout)
    db.session.commit()
    flash("スカウトを送りました！")
    # ページ更新
    return redirect(url_for("show_scout", user_id=company_id))


###学生向けの関数など
# スカウトされた企業一覧の表示
@app.route("/scouted/<int:user_id>")
@is_logined
def show_scouted(user_id):
    scout = Scout.query.filter(Scout.student_id == user_id)
    return render_template(
        "scout/scout_list.html", user=session["user"], scouts = scout
    )

# スカウトを承諾/拒否する
@app.route("/scout_answer/<int:user_id>/<int:company_id>/<string:answer>")
@is_logined
def scout_answer(user_id, company_id, answer):
    # スカウト種類の特定
    scout = Scout.query.filter(Scout.student_id == user_id, Scout.company_id==company_id)
    #スカウト結果の格納(result変数の更新)
    #scout.result = answer.update({Scout.result: answer})
    db.session.query(Scout).filter(Scout.student_id==user_id, Scout.company_id==company_id).update({Scout.result: answer})
    # データベースの更新
    db.session.commit()
    if(answer=="success"): flash("スカウトを承諾しました！")
    elif(answer=="false"): flash("スカウトを拒否しました...")
    return render_template(
        "scout/scout_list.html", user=session["user"], scouts = Scout.query.filter(Scout.student_id == user_id)
    )


#####ここから未実装・未確認

# 特定の学生とのチャット
@app.route("/scout/<int:id>")
@is_logined
def scout_chats(id):
    scout = Scout.query.get(id)
    chats = (
        ScoutChat.query.filter(and_(Scout.student_id==scout.student_id, Scout.company_id==scout.company_id))
        .order_by(Chat.time_post.asc())
        .all()
    )
    # チャット画面に移動
    return render_template(
        "scout/scout_chats.html", user=session["user"], student=scout.student_id, student_name=scout.student_name, chats=chats
    )
