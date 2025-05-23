from flask import Flask
import os
from flask_migrate import Migrate


from models import db, create_table
from views import add_user


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
create_table(app)

migrate = Migrate(app, db)

add_user(app, engine=db)

if __name__ == "__main__":
    app.run(debug=True)
