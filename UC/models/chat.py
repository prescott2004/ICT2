from UC import db
from datetime import datetime
from UC.models.user import User
import re


# モデル: チャット
class Chat(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "chats"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # 投稿日時
    time_post = db.Column(db.DateTime, nullable=False)
    # 投稿ユーザ
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # 所属グループ(外部キー制約)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    # テキスト
    text = db.Column(db.Text)
    # ファイル
    file_name = db.Column(db.Text)

    # モデルが作成されたときの標準の動作を定義
    def __init__(
        self,
        user_id,
        group_id,
        time_post,
        text=None,
        file_name=None,
    ) -> None:
        self.user_id = user_id
        self.group_id = group_id
        self.time_post = time_post
        self.text = text
        self.file_name = file_name

    def get_time_post_str(self):
        return self.time_post.strftime("%Y/%m/%d %H:%M")

    def get_time_post_linkstr(self):
        return self.time_post.strftime("%Y%m%d%H%M%S")

    def get_user_name(self):
        user = User.query.get(self.user_id)
        return f"{user.name_last} {user.name_first}"

    def get_texts_with_url(self):
        results = []
        texts = re.split("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", self.text)
        for text in texts:
            results.append({"content": text, "is_url": False})
        urls = re.findall("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", self.text)
        pos = 0
        for i in range(len(results) - 1):
            results.insert(i + pos + 1, {"content": urls[i], "is_url": True})
            pos += 1

        print(results)
        return results
