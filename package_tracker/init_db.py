# from mariadb.models import Tracker, Package, Warehouse, SessionPrimary, SessionSecondary, DeliveryMan, Smartphone, db
# from app import db
from mariadb.models import *

# def add_tracker():
#     db.session.commit()

def clean_mariadb():
    print("clean db")
    db.session.query(Package).delete()
    db.session.query(Warehouse).delete()
    db.session.commit()

    
def add_package():
    print("add packages")
    db.session.add(Package(destination='Nantes', status='new', tracking_number='10000'))
    db.session.add(Package(destination='Rennes', status='in delivering', tracking_number='10001'))
    db.session.add(Package(destination='Reims', status='delivered', tracking_number='10002'))
    db.session.commit()

def add_warehouse():
    print("add warehouses")
    db.session.add(Warehouse(name='warehouse one'))
    db.session.add(Warehouse(name='warehouse two'))
    db.session.add(Warehouse(name='warehouse three'))
    db.session.commit()

def add_sessionprimary():
    db.session.add(SessionPrimary(package='1', tracker='1', warehouse='1', status='new', time='17:00'))
    db.session.add(SessionPrimary(package='2', tracker='2', warehouse='2', status='in the warehouse', time='17:30'))
    db.session.add(SessionPrimary(package='3', tracker='3', warehouse='3', status='out of the warehouse', time='18:00'))
    db.session.commit()

def add_sessionsecondary():
    db.session.add(SessionSecondary(package='1', delivery_man='1', time='17:00'))
    db.session.add(SessionSecondary(package='2', delivery_man='2', time='17:30'))
    db.session.add(SessionSecondary(package='3', delivery_man='3', time='18:00'))
    db.session.commit()

def add_delivery_man():
    db.session.add(DeliveryMan(smartphone='1'))
    db.session.add(DeliveryMan(smartphone='2'))
    db.session.add(DeliveryMan(smartphone='3'))
    db.session.commit()

def add_smartphone():
    db.session.add(Smartphone(latitude='47.21476', longitude='-1.55589'))
    db.session.add(Smartphone(latitude='48.11208', longitude='-1.68376'))
    db.session.add(Smartphone(latitude='49.24343', longitude='4.06231'))
    db.session.commit()
