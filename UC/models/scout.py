from UC import db
from datetime import datetime

# モデル: チャット
class Scout(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "scout"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # 投稿日時
    time_post = db.Column(db.DateTime, nullable=False)
    # スカウト企業
    company_id = db.Column(db.Integer, nullable=False)
    # 被スカウト学生のid
    student_id = db.Column(db.Integer, nullable=False)
    # 被スカウト学生の氏名
    student_name = db.Column(db.String(100), nullable=False)
    # スカウト企業の名前
    company_name = db.Column(db.String(100), nullable=False)
    # スカウト結果(スカウト中："waiting", 成功："success", 失敗："false")
    result = db.Column(db.String(10), nullable=False)
    # モデルが作成されたときの標準の動作を定義
    def __init__(self, company_id, student_id, company_name, student_name) -> None:
        self.time_post = datetime.now()
        self.company_id = company_id
        self.student_id = student_id
        self.company_name = company_name
        self.student_name = student_name
        self.result = "waiting"

    def get_time_post_str(self):
        return self.time_post.strftime("%Y/%m/%d %H:%M")
