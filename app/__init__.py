from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment variable

# Register Blueprints
from app.blueprints.accounts import accounts
from app.blueprints.tickers import tickers
from app.blueprints.transactions import transactions
app.register_blueprint(accounts)
app.register_blueprint(tickers)
app.register_blueprint(transactions)


from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)

