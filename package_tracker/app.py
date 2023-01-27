from flask import Flask
from flask import render_template, abort
from flask_apscheduler import APScheduler
from mariadb.models import db
from publishers.mqtt_pub import mqtt_change_warehouse
from publishers.amqp_pub import amqp_publish
from init_db import clean_mariadb, add_package, add_warehouse
import random

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mariadb'
app.config['SECRET_KEY'] = "abcdef"
db.init_app(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from mariadb.models import Tracker, Package, Warehouse, SessionPrimary, SessionSecondary, DeliveryMan, Smartphone

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
    warehouses = Warehouse.query.all()
    warehouses_list = []
    for warehouse in warehouses:
        warehouses_list.append(warehouse.name)
    return warehouses_list



@app.route("/api/v1/change_warehouse", methods=['POST'])
def change_warehouse():
    tracking_number = request.args.get('tracking_number', None)
    new_warehouse = request.args.get('warehouse', None) 
    # If exists, update former primary session to indicated that the package left it
    # create new row in primary session table with the new info (warehouse name and tracking number)
    return result



@app.route("/api/v1/tool/change_warehouse", methods=['POST'])
def tool_change_warehouse():
    tracking_number = request.args.get('tracking_number', None)
    new_warehouse = request.args.get('warehouse', None) 
    if not tracking_number or not new_warehouse:
        abort(404)
    result = mqtt_change_warehouse(new_warehouse, tracking_number)
    return result


@app.route("/api/v1/tool/start_delivery", methods=['POST'])
def tool_start_delivery():
    tracking_number = request.args.get('tracking_number', None)
    if not tracking_number:
        abort(404)
    # Get list of deliveryman ids and select one randomly
    data_to_send = {
        "latitude": round(random.uniform(-90, 90), 6),
        "longitude": round(random.uniform(-180, 180), 6),
        # To complete with the choosen deliveryman id
    }
    amqp_publish("geoloc", data_to_send)
    # Quit warehouse => PUBLISHER MQTT to ask to close last primary_session & to deattach tracker and package
    # return if the change request has been successfuly made in json


@app.route("/test")
def test():
    mqtt_change_warehouse("warehouse one", "test message")
    return "Done"

# @app.route("/test")
# def test():
#     amqp_publish("WAREFIRST", {"test message":"test vak"})
#     return "Done"


@app.route("/api/v1/populate_db", methods=['GET'])
def populate_db():
    add_package()
    add_warehouse()
    return "OK"


@app.route("/api/v1/clean_db", methods=['GET'])
def clean_db():
    clean_mariadb()
    return "OK"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)