from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from app.db.model import *

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mariadb'
app.config['SECRET_KEY'] = "abcdef"
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)