from flask import Flask
from flask import render_template, abort, request
from flask_apscheduler import APScheduler
from mariadb.models import db
from publishers.mqtt_pub import mqtt_change_warehouse
from publishers.amqp_pub import amqp_publish
from init_db import clean_mariadb, add_package, add_warehouse
import random
import datetime.datetime

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


def interval_task(smartphone_id):
    data_to_send = {
        "latitude": round(random.uniform(-90, 90), 6),
        "longitude": round(random.uniform(-180, 180), 6),
        "smartphone_id": smartphone_id
    }
    amqp_publish("main", data_to_send)


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
    if not tracking_number or not new_warehouse:
        abort(404)
    package = db.session.query(Package).filter(Package.tracking_number==tracking_number).first()
    ps = db.session.query(SessionPrimary).filter(SessionPrimary.tracking_number==tracking_number, SessionPrimary.status == "in progress").first()
    if ps:
        ps.status = "archived"
        tracker = ps.tracker
        db.session.commit()
    else:
        tracker = db.session.query(Tracker).filter(Tracker.status=="free").first()
        if not tracker:
            print("no free tracker")
            abort(404)
        tracker.status = "busy"
        package.status = "in transit"
    warehouse = db.session.query(Warehouse).filter(Warehouse.name==new_warehouse).first()
    db.session.add(SessionPrimary(package=package, tracker=tracker, warehouse=warehouse, status='in progress', date=datetime.now()))
    db.session.commit()
    return {
        "package": package.tracking_number,
        "warehouse": warehouse.name,
        "tracker": tracker.id
    }


@app.route("/api/v1/start_delivery", methods=['POST'])
def start_delivery():
    tracking_number = request.args.get('tracking_number', None)
    if not tracking_number:
        abort(404)

    list_of_dlvm = db.session.query(DeliveryMan).all()
    nb_of_dlvm = len(list_of_dlvm)
    choosen_dlvm = random.randrange(nb_of_dlvm)
    dlvm = list_of_dlvm[choosen_dlvm]

    latitude = round(random.uniform(-90, 90), 6)
    longitute = round(random.uniform(-180, 180), 6)

    ps = db.session.query(SessionPrimary).filter(SessionPrimary.tracking_number==tracking_number, SessionPrimary.status == "in progress").first()
    ps.status = "archived"
    tracker = ps.tracker
    tracker.status = "free"
    db.session.commit()

    package = db.session.query(Package).filter(Package.tracking_number==tracking_number).first()
    package.status = "out for delivery"
    db.session.add(SessionSecondary(package=package, delivery_man=dlvm.id, status='in progress', date=datetime.now()))
    db.session.commit()
    smartphone = dlvm.smartphone
    scheduler.add_job(id=f'id-{tracker.tracking_number}', func=lambda: interval_task(smartphone.id), trigger='interval', seconds=60)
    return {
        "package": package.tracking_number,
        "delivery_man": delivery_man.id
    }


@app.route("/api/v1/stop_delivery", methods=['POST'])
def stop_delivery():
    tracking_number = request.args.get('tracking_number', None)
    if not tracking_number:
        abort(404)

    package = db.session.query(Package).filter(Package.tracking_number==tracking_number).first()
    package.status = "delivered"
    ss = db.session.query(SessionSecondary).filter(SessionSecondary.tracking_number==tracking_number, SessionPrimary.status == "in progress").first()
    ss.status = "archived"
    db.session.commit()
    scheduler.resume_job(id=f'id-{tracker.tracking_number}')

    return "OK"


@app.route("/api/v1/update_geoloc", methods=['POST'])
def update_geoloc():
    latitude = request.args.get('latitude', None)
    longitude = request.args.get('longitude', None)
    smartphone_id = request.args.get('smartphone_id', None)
    if not latitude or not longitude or not smartphone_id:
        abort(404)

    smartphone = db.session.query(Smartphone).filter(Smartphone.id==smartphone_id).first()
    smartphone.latitude = latitude
    smartphone.longitude = longitude
    db.session.commit()
    return {
        "latitude": latitude,
        "longitude": longitude,
        "smartphone_id": smartphone_id,
    }



@app.route("/api/v1/simulate/change_warehouse", methods=['POST'])
def simulate_change_warehouse():
    tracking_number = request.args.get('tracking_number', None)
    new_warehouse = request.args.get('warehouse', None) 
    if not tracking_number or not new_warehouse:
        abort(404)
    result = mqtt_change_warehouse(new_warehouse, tracking_number)
    return result


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