import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Customer, Game, Listing
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database and seeds sample data")
def init():
    initialize()
    # --- Seed sample data ---
    # Create sample customers
    kristian = Customer(username="kristian", password="kristianpass")
    kendell = Customer(username="Kendell", password="kendellpass")
    admin = User(username="admin", password="adminpass")
    db.session.add(kristian)
    db.session.add(admin)
    db.session.add(kendell)
    db.session.commit()

    # Create sample games
    chess = Game(title="Chess")
    monopoly = Game(title="Monopoly")
    db.session.add(chess)
    db.session.add(monopoly)
    db.session.commit()

    # Create sample listings
    listing1 = Listing(game_id=chess.id, owner_id=kristian.id, condition="New", price=25.0)
    listing2 = Listing(game_id=monopoly.id, owner_id=kendell.id, condition="Used", price=15.0)
    db.session.add(listing1)
    db.session.add(listing2)
    db.session.commit()
    print('database initialized and seeded with sample data')

@app.cli.command("listGame", help= "uploads a game listing")
def listGame():
    games = Game.query.all()
    print(games)
    game = input("Enter the game title you want to list: ")
    condition = input("Enter the condition of the game (e.g., New, Like New, Used): ")
    price = float(input("Enter the price for the game: "))
    username = input("Enter your username: ")
    user = User.query.filter_by(username=username).first()
    try:
        if not user:
            raise Exception("User does not exist. Please create an account first.")
    except Exception as e:
        print(f"Error: {e}")
        return
    newGame = Game(title=game)
    db.session.add(newGame)
    db.session.commit()  # Commit to get the new game's ID
    newListing = Listing(game_id=newGame.id, owner_id=user.id, condition=condition, price=price)
    db.session.add(newListing)
    db.session.commit()
    print(f'Game "{game}" listed successfully with ID {newGame.id} by user "{username}".')

# @app.cli.command("returnGame", help="Returns a rented game")
# def returnGame():
#     username = input("Enter your username: ")
#     user = User.query.filter_by(username=username).first()
#     try:
#         if not user:
#             raise Exception("User does not exist.")
#         if not isinstance(user, Customer):
#             raise Exception("Only customers can return games.")
#     except Exception as e:
#         print(f"Error: {e}")
#         return

#     rentals = user.rentals
#     if not rentals:
#         print("You have no rentals.")
#         return

#     print("Your Rentals:")
#     for rental in rentals:
#         listing = Listing.query.get(rental.listingID)
#         game = Game.query.get(listing.game_id) if listing else None
#         status = "Returned" if rental.returnDate else "Not Returned"
#         print(f'Rental ID: {rental.id}, Game: {game.title if game else "Unknown"}, Status: {status}')

#     rental_id = int(input("Enter the Rental ID of the game you want to return: "))
#     rental_to_return = next((r for r in rentals if r.id == rental_id), None)
#     try:
#         if not rental_to_return:
#             raise Exception("Rental does not exist.")
#         if rental_to_return.returnDate is not None:
#             raise Exception("Game has already been returned.")
        
#         rental_to_return.returnDate = datetime.utcnow()
#         listing = Listing.query.get(rental_to_return.listingID)
#         if listing:
#             listing.set_Availability(True)  # Mark the listing as available again
#         db.session.commit()
#         print(f'Game with Rental ID {rental_id} returned successfully.')
#     except Exception as e:
#         print(f"Error when trying to return a game: {e}")
#         return None

@app.cli.command("list-games", help="Lists all games in the database")
def list_games():
    games = Game.query.all()
    for game in games:
        print(f'ID: {game.id}, Title: {game.title}, Description: {game.description}')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)