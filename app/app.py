from flask import Flask
from flask import render_template, abort
from mariadb.models import db

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mariadb'
app.config['SECRET_KEY'] = "abcdef"
db.init_app(app)

from mariadb.models import Tracker

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/track_package")
def track_package():
    return render_template("track_package.html")



@app.route("/api/v1/package", methods=['GET'])
def get_package():
    tracking_number = request.args.get('tracking_number', None)
    if not tracking_number:
        abort(404)
    # Search package status
    # Based on status, trigger action
    # new => return info message
    # primary_session => get_primary_session_info
    # secondary_session => get_secondary_session_info
    # delivered
    """
        {
            "status": "",
            "message": ""
            "additional_data": ...
        }
    """

@app.route("/api/v1/warehouses", methods=['GET'])
def get_warehouses():
    # Return list of warehouses



@app.route("/api/v1/change_warehouse", methods=['POST'])
def change_warehouse():
    tracking_number = request.args.get('tracking_number', None)
    new_warehouse = request.args.get('warehouse', None) 
    if not tracking_number or not new_warehouse:
        abort(404)
    # Change warehouse
    # return status in json



# if __name__ == '__main__':
with app.app_context():
    db.create_all()
app.run(debug = True)