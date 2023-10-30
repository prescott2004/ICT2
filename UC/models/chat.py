from UC import db
from datetime import datetime


# モデル: チャット
class Chat(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "chat"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True)
    #
