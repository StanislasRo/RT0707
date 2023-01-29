# from mariadb.models import Tracker, Package, Warehouse, SessionPrimary, SessionSecondary, DeliveryMan, Smartphone, db
# from app import db
from mariadb.models import *

# def add_tracker():
#     db.session.commit()

def clean_mariadb():
    print("clean db")
    db.session.query(SessionPrimary).delete()
    db.session.commit()
    db.session.query(SessionSecondary).delete()
    db.session.commit()
    db.session.query(Package).delete()
    db.session.query(Tracker).delete()
    db.session.query(Warehouse).delete()
    db.session.query(DeliveryMan).delete()
    db.session.commit()
    db.session.query(Smartphone).delete()
    db.session.commit()

def add_db():
    trackerone = Tracker(status='free')
    trackertwo = Tracker(status='free')
    trackerthree = Tracker(status='free')
    packageone = Package(destination='Nantes', status='new', tracking_number='10000')
    packagetwo = Package(destination='Rennes', status='new', tracking_number='10001')
    packagethree = Package(destination='Reims', status='new', tracking_number='10002')
    warehouseone = Warehouse(name='warehouse one')
    warehousetwo = Warehouse(name='warehouse two')
    warehousethree = Warehouse(name='warehouse three')
    smartphoneone = Smartphone(latitude='47.21476', longitude='-1.55589')
    smartphonetwo = Smartphone(latitude='48.11208', longitude='-1.68376')
    smartphonethree = Smartphone(latitude='49.24343', longitude='4.06231')
    db.session.add_all([smartphoneone,smartphonetwo,smartphonethree])
    db.session.commit()
    deliverymanone = DeliveryMan(smartphone=smartphoneone.id)
    deliverymantwo = DeliveryMan(smartphone=smartphonetwo.id)
    deliverymanthree = DeliveryMan(smartphone=smartphonethree.id)
    db.session.add_all([trackerone,trackertwo,trackerthree])
    db.session.add_all([packageone,packagetwo,packagethree])
    db.session.add_all([warehouseone,warehousetwo,warehousethree])
    
    db.session.add_all([deliverymanone,deliverymantwo,deliverymanthree])
    db.session.commit()
