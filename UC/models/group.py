from UC import db
from datetime import datetime


# モデル: グループ
class Group(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "group"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True)
    # タイトル
    title = db.Column(db.Text)
