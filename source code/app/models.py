from sqlalchemy import sql
from app import db

class Incident(db.Model):
	__tablename__ = "incident"
	id = db.Column("id", db.BigInteger(), 
		primary_key = True, nullable = False)
	international = db.Column("international", db.Integer(), nullable = False)
	property_damage = db.Column("property_damage", db.Integer(), nullable = False)
	nwound = db.Column("nwound", db.Integer())
	nkill = db.Column("nkill", db.Integer())
	date = db.Column("date", db.Date())

class Location(db.Model):
	__tablename__ = "location"
	latitude = db.Column("latitude", db.Numeric(), 
		primary_key = True, nullable = False)
	longitude = db.Column("longitude", db.Numeric(),
		primary_key = True, nullable = False)
	country = db.Column("country", db.String(256))
	prov_state = db.Column("prov_state", db.String(256))
	city = db.Column("city", db.String(256))

class Happened(db.Model):
	__tablename__ = "happened"
	incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("Incident.id"), 
		nullable = False, primary_key = True)
	latitude = db.Column("latitude", db.Numeric(), 
		db.ForeignKey("Location.latitude"),nullable = False)
	longitude = db.Column("longitude", db.Numeric(), 
		db.ForeignKey("Location.longitude"),nullable = False)

class InitiatedBy(db.Model):
	__tablename__ = "initiatedBy"
	incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("Incident.id"), 
		nullable = False, primary_key = True)
	perpetrator_name = db.Column("perpetrator_name", db.String(256), nullable = False)

class Used(db.Model):
	__tablename__ = "used"
	incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("Incident.id"), 
		nullable = False, primary_key = True)
	weapon_type = db.Column("weapon_type", db.String(256), nullable = False)

class Targeted(db.Model):
	__tablename__ = "targeted"
	incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("Incident.id"), 
		nullable = False, primary_key = True)
	victim_type = db.Column("victim_type", db.String(256), nullable = False)
	subtype = db.Column("subtype", db.String(256), nullable = False)
	target = db.Column("target", db.String(500), nullable = False)

class Comment(db.Model):
	__tablename__ = "comment"
	user_id = db.Column("user_id", db.Sequence('user_id_seq'), nullable = False, primary_key = True)
	name = db.Column("name",db.String(20), nullable = False)
	message = db.Column("message", db.String(200), nullable = False)
