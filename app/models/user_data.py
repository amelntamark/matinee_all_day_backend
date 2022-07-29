from app import db


class UserData(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    seen_it = db.Column(db.String)
