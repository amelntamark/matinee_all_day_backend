from app import db


class Movie(db.Model):
    mad_database_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String)
    overview = db.Column(db.String)
    release_date = db.Column(db.String)
    poster = db.Column(db.String)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    session = db.relationship(
        "Session", back_populates="movies")
