from UC import db
from datetime import datetime


# モデル: チャット
class Chat(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "chat"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True)
    # 投稿日時
    time_post = db.Column(db.DateTime)
    # テキスト
    text = db.Column(db.Text)
    # 所属グループ
    group = db.relationship("Group", backref="chat")
