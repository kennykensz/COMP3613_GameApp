from App.database import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __init__(self, title, description=None):
        self.title = title

    def __repr__(self):
        return f'<Game {self.id} {self.title} {self.description}>'