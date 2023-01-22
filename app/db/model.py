from app.app import db
from sqlalchemy.ext.declarative import relationship

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, primary_key=True)

class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)    
    destination = db.Column(db.String(length=100))
    statut = db.Column(db.Integer, primary_key=True)  

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)    
    queue_name = db.Column(db.String(length=100))

class SessionPrimary(db.Model):
    __tablename__ = 'session_primary'
    id = db.Column(db.Integer, primary_key=True)    
    queue_name = db.Column(db.String(length=100))
    tracker = db.Column(db.Integer, db.ForeignKey('tracker.id'))
    package = db.Column(db.Integer, db.ForeignKey('package.id'))
    warehouse = db.Column(db.Integer, db.ForeignKey('warehouse.id'))

class SessionSecondary(db.Model):
    __tablename__ = 'session_secondary'
    id = db.Column(db.Integer, primary_key=True)    
    queue_name = db.Column(db.String(length=100))
    package = db.Column(db.Integer, db.ForeignKey('package.id'))
    delivery_man = db.Column(db.Integer, db.ForeignKey('delivery_man.id'))

class DeliveryMan(db.Model):
    __tablename__ = 'delivery_man'
    id = db.Column(db.Integer, primary_key=True)
    smartphone = db.Column(db.Integer, db.ForeignKey('smartphone.id'))

class Smartphone(db.Model):
    __tablename__ = 'smartphone'
    id = db.Column(db.Integer, primary_key=True)    
    latitude = db.Column(db.Numeric(precision=9, scale=6))
    longitude = db.Column(db.Numeric(precision=9, scale=6))