from flask_blog import db
from datetime import datetime


# モデル: 記事
class Entry(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "entries"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True)
    # タイトル(50文字以内, 重複なし)
    title = db.Column(db.String(50), unique=True)
    # 本文
    text = db.Column(db.Text)
    # 投稿日時
    created_at = db.Column(db.Datetime)

    # モデルが作成されたときの標準の動作を定義
    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text
        self.created_at = datetime.utcnow()

    # 実際に記事モデルが参照されたときのコンソールでの出力形式
    def __repr__(self):
        return "<Entry id:{} title:{} text:{}>".format(self.id, self.title, self.text)
