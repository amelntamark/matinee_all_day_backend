from app import db


class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String)
    era = db.Column(db.String)
    runtime = db.Column(db.String)
