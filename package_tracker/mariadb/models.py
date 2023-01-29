from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(length=100), default='free') # free / busy

class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)    
    destination = db.Column(db.String(length=100))
    status = db.Column(db.String(length=100), default='new')
    tracking_number = db.Column(db.Integer)

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(length=100))

class SessionPrimary(db.Model):
    __tablename__ = 'session_primary'
    id = db.Column(db.Integer, primary_key=True)    
    package = db.Column(db.Integer, db.ForeignKey('package.id'), unique=True, nullable=True)
    tracker = db.Column(db.Integer, db.ForeignKey('tracker.id'), unique=True, nullable=True)
    warehouse = db.Column(db.Integer, db.ForeignKey('warehouse.id'), unique=True, nullable=True)
    status = db.Column(db.String(length=100)) # in progress / archived
    date = db.Column(db.DateTime(timezone=True)) 

class SessionSecondary(db.Model):
    __tablename__ = 'session_secondary'
    id = db.Column(db.Integer, primary_key=True)    
    package = db.Column(db.Integer, db.ForeignKey('package.id'), unique=True, nullable=True)
    delivery_man = db.Column(db.Integer, db.ForeignKey('delivery_man.id'), unique=True, nullable=True)
    status = db.Column(db.String(length=100)) # in progress / archived
    date = db.Column(db.DateTime(timezone=True))

class DeliveryMan(db.Model):
    __tablename__ = 'delivery_man'
    id = db.Column(db.Integer, primary_key=True)
    smartphone = db.Column(db.Integer, db.ForeignKey('smartphone.id'), unique=True, nullable=True)

class Smartphone(db.Model):
    __tablename__ = 'smartphone'
    id = db.Column(db.Integer, primary_key=True)    
    latitude = db.Column(db.Numeric(precision=9, scale=6))
    longitude = db.Column(db.Numeric(precision=9, scale=6))