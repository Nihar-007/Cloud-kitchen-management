from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ASDHADNHD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/restaurant'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.jpeg','.jpg','.png'] 

# app.config['SQLALCHEMY_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# ALL the classes where here

from routes import *
# all routes are here


if __name__ == '__main__':
    app.run(debug=True)

