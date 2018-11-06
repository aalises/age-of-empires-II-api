from flask import redirect
from sqlalchemy_utils import database_exists
from config import APP_CONFIG, API_PREFIX, DB_NAME
from api import create_app
from db.populate_tables import populate_db
from db import db

app = create_app(APP_CONFIG)

@app.before_first_request
def create_tables():
    if not database_exists(DB_NAME):
        db.create_all()
        populate_db()

@app.route(API_PREFIX)
@app.route("/")
def redirect_to_civilizations():
    return redirect("{}/civilizations".format(API_PREFIX), code=302)


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
