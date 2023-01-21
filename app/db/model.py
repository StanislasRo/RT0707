from app.app import db
from sqlalchemy.ext.declarative import relationship

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.Integer, primary_key=True)

class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)    
    destination = db.Column(db.String(length=100))

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)    
    queue_name = db.Column(db.String(length=100))

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)    
    queue_name = db.Column(db.String(length=100))