from flask import Flask
from flask import render_template, abort, request
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
    return render_template("tracking.html")


@app.route("/api/v1/package", methods=['GET'])
def get_package():
    tracking_number = request.args.get('tracking-number', None)
    if not tracking_number:
        abort(404)
    package = db.session.query(Package).filter(Package.tracking_number==tracking_number).first()
    if package:
        if package.status == "new":
            return {
                "status": "new",
                "message": "The package has not yet been picked up",
                "additional_data": ""
            }
        elif package.status == "in transit":
            primary_session_info = get_primary_session_info(package.id)
            return {
                "status": "in transit",
                "message": "The package is transiting in: ",
                "additional_data": primary_session_info
            }
        elif package.status == "out for delivery":
            secondary_session_info = get_secondary_session_info(package.id)
            return {
                "status": "out for delivery",
                "message": f"The delivery man is currently at Latitude: {lat}, Longitude: {lon}",
                "additional_data": secondary_session_info
            }
        elif package.status == "delivered":
            return {
                "status": "delivered",
                "message": f"The packet has already been delivered.",
                "additional_data": ""
            }
    return {
            "status": "Package not found",
            "message": "",
            "additional_data": ""
        }
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
    # If primary sessions exists with this tracking number, update former primary session to indicated that the package left it
    # create new row in primary session table with the new info (warehouse name and tracking number)
    return result



@app.route("/api/v1/simulate/change_warehouse", methods=['POST'])
def simulate_change_warehouse():
    tracking_number = request.args.get('tracking_number', None)
    new_warehouse = request.args.get('warehouse', None) 
    if not tracking_number or not new_warehouse:
        abort(404)
    result = mqtt_change_warehouse(new_warehouse, tracking_number)
    return result


@app.route("/api/v1/simulate/start_delivery", methods=['POST'])
def simulate_start_delivery():
    tracking_number = request.args.get('tracking_number', None)
    if not tracking_number:
        abort(404)
    # Get list of deliveryman ids and select one randomly
    data_to_send = {
        "tracking_number": tracking_number,
        "latitude": round(random.uniform(-90, 90), 6),
        "longitude": round(random.uniform(-180, 180), 6),
        # To complete with the choosen deliveryman id
    }
    amqp_publish("main", data_to_send)
    return "OK"
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



def get_primary_session_info(fk_package):
    # List warehouse + status + time
    info_about_package = []
    list_of_ps = db.session.query(SessionPrimary).filter(SessionPrimary.package==fk_package).order_by(SessionPrimary.date)
    for ps in list_of_ps:
        info_about_package.append({
            "warehouse": ps.warehouse,
            "status": ps.status,
            "date": ps.date
        })
    return info_about_package



def get_secondary_session_info(fk_package):
    # List warehouse + status + time
    info_about_package = []
    list_of_ss = db.session.query(SessionSecondary).filter(SessionSecondary.package==fk_package).order_by(SessionSecondary.date)
    for ss in list_of_ss:
        delivery_man = db.session.query(DeliveryMan).filter(DeliveryMan.id==ss.delivery_man)
        smartphone_geoloc = db.session.query(Smartphone).filter(Smartphone.id==delivery_man.smartphone)
        info_about_package.append({
            "lat": smartphone_geoloc.latitude,
            "lon": smartphone_geoloc.longitude,
            "status": ps.status,
            "date": ps.date
        })
    return info_about_package



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)