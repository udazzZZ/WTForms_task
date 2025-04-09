from flask import Flask
from models import db, create_table
from views import add_user

import os


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
create_table(app)

add_user(app, engine=db)

if __name__ == "__main__":
    app.run(debug=True)
