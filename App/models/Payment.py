from App.database import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paymentDate = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def getAmount(self):
        return self.amount

    def toJSON(self):
        return {
            'id': self.id,
            # 'rental_id': self.rental_id,
            'customer_id': self.customer_id,
            'paymentDate': self.paymentDate.isoformat(),
            'amount': self.amount
        }