from App.database import db
import enum


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    condition = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    

    game = db.relationship('Game', backref=db.backref('listings', lazy=True))
   # owner = db.relationship('User', backref=db.backref('listings', lazy=True))  

    def __init__(self, game_id, owner_id, condition, price):
        self.game_id = game_id
        self.condition = condition
        self.price = price
        self.owner_id = owner_id    

    def set_Availability(self, status):
        self.availability = status