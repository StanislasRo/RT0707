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

def add_db():
    trackerone = Tracker(status='busy')
    trackertwo = Tracker(status='busy')
    trackerthree = Tracker(status='busy')
    packageone = Package(destination='Nantes', status='new', tracking_number='10000')
    packagetwo = Package(destination='Rennes', status='in delivering', tracking_number='10001')
    packagethree = Package(destination='Reims', status='delivered', tracking_number='10002')
    warehouseone = Warehouse(name='warehouse one')
    warehousetwo = Warehouse(name='warehouse one')
    warehousethree = Warehouse(name='warehouse one')
    smartphoneone = Smartphone(latitude='47.21476', longitude='-1.55589')
    smartphonetwo = Smartphone(latitude='48.11208', longitude='-1.68376')
    smartphonethree = Smartphone(latitude='49.24343', longitude='4.06231')
    deliverymanone = DeliveryMan(smartphone=smartphoneone)
    deliverymantwo = DeliveryMan(smartphone=smartphonetwo)
    deliverymanthree = DeliveryMan(smartphone=smartphonethree)
    db.session.add_all([trackerone,trackertwo,trackerthree])
    db.session.add_all([packageone,packagetwo,packagethree])
    db.session.add_all([warehouseone,warehousetwo,warehousethree])
    db.session.add_all([deliverymanone,deliverymantwo,deliverymanthree])
    db.session.add_all([smartphoneone,smartphonetwo,smartphonethree])
    db.session.commit()
