from UC import db


# モデル: ユーザ
class User(db.Model):
    # 実際のデータベースに格納されるテーブルの名前
    __tablename__ = "users"
    # id(プライマリーキー)
    id = db.Column(db.Integer, primary_key=True)
    # 姓
    name_last = db.Column(db.String(50))
    # 名
    name_first = db.Column(db.String(50))
    # アドレス
    email = db.Column(db.String(100), unique=True)
    # パスワード
    password = db.Column(db.String(100))

    # モデルが作成されたときの標準の動作を定義
    def __init__(self, name_last=None, name_first=None, email=None, password=None):
        self.name_last = name_last
        self.name_first = name_first
        self.email = email
        self.password = password

    # 実際に記事モデルが参照されたときのコンソールでの出力形式
    def __repr__(self):
        return "<Entry id:{} name:{} {} email:{}>".format(
            self.id, self.name_last, self.name_first, self.email
        )

    # セッションを保存する場合の形式
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}