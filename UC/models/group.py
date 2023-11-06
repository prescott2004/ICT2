from UC import db
from datetime import datetime


# モデル: グループ
class Group(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "groups"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # 作成日時
    time_create = db.Column(db.DateTime, nullable=False)
    # タイトル
    title = db.Column(db.Text, nullable=False)
    # Chatテーブルにgroupという名前で参照させてあげることを宣言
    chat = db.relationship("Chat", backref="groups")

    def __init__(self,title) -> None:
        self.time_create = datetime.now()
        self.title = title
    
