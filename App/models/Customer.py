from App.database import db
from .user import User
from .Listing import Listing
from .Payment import Payment
from .Rental import Rental
from datetime import datetime

class Customer(User):
    listings = db.relationship('Listing', backref='owner', lazy=True)
    payments = db.relationship('Payment', backref='customer', lazy=True)
    rentals = db.relationship('Rental', backref='renter', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)  

    def listGame(self, game, condition, price):
        new_listing = Listing(game_id=game, owner_id=self.id, condition=condition, price=price)
        self.listings.append(new_listing)
        db.session.add(new_listing)
        db.session.commit()
        return new_listing

    def rentGame(self, listing):
        try:
            if not listing:
                raise Exception("Listing does not exist.")
            if listing.availability:  # Check if the listing is available
                new_rental = Rental(renterID=self.id, listingID=listing.id, rentalDate=datetime.utcnow())
                self.rentals.append(new_rental)
                listing.set_Availability(False)  # Mark the listing as unavailable since the customer is now purchasing this listing
                db.session.add(new_rental)
                db.session.commit()
                return new_rental
            else:
                raise Exception("Listing is not available for rent.")
        except Exception as e:
            print(f"Error when trying to rent a game: {e}")
            return None

    def returnGame(self, rental):
        try:
            if not rental:
                raise Exception("Rental does not exist.")
            if rental.returnDate is not None:
                raise Exception("Game has already been returned.")
            rental.returnDate = datetime.utcnow()
            listing = Listing.query.get(rental.listingID)
            if listing:
                listing.set_Availability(True)  # Mark the listing as available again
            db.session.commit()
            return rental
        except Exception as e:
            print(f"Error when trying to return a game: {e}")
            return None
        

        # def makePayment(self, amount):
        # new_payment = Payment(customer_id=self.id, paymentDate=datetime.utcnow(), amount=amount)
        # self.payments.append(new_payment)
        # db.session.add(new_payment)
        # db.session.commit()
        # return new_payment


