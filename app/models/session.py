from app import db


class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String)
    era = db.Column(db.String)
    runtime = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user_data.user_id'))
    user_data = db.relationship(
        "UserData", backref=db.backref("user_data", uselist=False))
    movies = db.relationship(
        "Movie", back_populates="session"
    )
