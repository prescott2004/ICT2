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
    # 作成ユーザ
    user_id_host = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # タイトル
    title = db.Column(db.Text, nullable=False)
    # 説明
    description = db.Column(db.Text)
    # Chatテーブルにgroupという名前で参照させてあげることを宣言
    chat = db.relationship("Chat", backref="groups")

    def __init__(self, user_id_host, title, description) -> None:
        self.time_create = datetime.now()
        self.user_id_host = user_id_host
        self.title = title
        self.description = description

    def show_description(self):
        if len(self.description) > 200:
            return self.description[:200] + "..."
        return self.description
