from App.database import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    renterID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listingID = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)

    rentalDate = db.Column(db.DateTime, nullable=False)
    returnDate = db.Column(db.DateTime, nullable=True)

    def toJSON(self):
        return {
            'id': self.id,
            'renterID': self.renterID,
            'listingID': self.listingID,
            'rentalDate': self.rentalDate.isoformat(),
            'returnDate': self.returnDate.isoformat() if self.returnDate else None
        }
