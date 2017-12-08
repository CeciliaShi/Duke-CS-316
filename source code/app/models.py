from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql, orm


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

class Incident(db.Model):
        __tablename__ = "incident"
        id = db.Column("id", db.BigInteger(),
                primary_key = True, nullable = False)
        international = db.Column("international", db.Integer(), nullable = False)
        property_damage = db.Column("property_damage", db.Integer(), nullable = False)
        nwound = db.Column("nwound", db.Integer())
        nkill = db.Column("nkill", db.Integer())
        date = db.Column("date", db.Date())
        targeted = orm.relationship("Targeted", uselist=False, back_populates="incident")
        happened = orm.relationship("Happened", uselist=False, back_populates="incident")
        belongedto = orm.relationship("BelongedTo", uselist=False, back_populates="incident")


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
        incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("incident.id"),
                nullable = False, primary_key = True)
        latitude = db.Column("latitude", db.Numeric(),
                db.ForeignKey("location.latitude"),nullable = False)
        longitude = db.Column("longitude", db.Numeric(),
                db.ForeignKey("location.longitude"),nullable = False)
        incident = orm.relationship("Incident", back_populates="happened")


class InitiatedBy(db.Model):
        __tablename__ = "initiatedby"
        incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("incident.id"),
                nullable = False, primary_key = True)
        perpetrator_name = db.Column("perpetrator_name", db.String(256), nullable = False)

class Used(db.Model):
        __tablename__ = "used"
        incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("incident.id"),
                nullable = False, primary_key = True)
        weapon_type = db.Column("weapon_type", db.String(256), nullable = False)

class BelongedTo(db.Model):
        __tablename__ = "belongedto"
        incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("incident.id"),
                nullable = False, primary_key = True)
        attack_type = db.Column("attack_type", db.String(256), nullable = False)
        succussful_attack = db.Column("succussful_attack", db.Integer(), nullable = False)
        suicide_attack = db.Column("suicide_attack", db.Integer(), nullable = False)
        incident = orm.relationship("Incident", back_populates="belongedto")

class Targeted(db.Model):
        __tablename__ = "targeted"
        incident_id = db.Column("incident_id", db.BigInteger(), db.ForeignKey("incident.id"),
                nullable = False, primary_key = True)
        victim_type = db.Column("victim_type", db.String(256), nullable = False)
        subtype = db.Column("subtype", db.String(256), nullable = False)
        target = db.Column("target", db.String(500), nullable = False)
        incident = orm.relationship("Incident", back_populates="targeted")

class Comment(db.Model):
        __tablename__ = "comment"
        user_id = db.Column("user_id", db.Sequence('user_id_seq'), nullable = False, primary_key=True)
        name = db.Column("name",db.String(20), nullable = False)
        message = db.Column("message", db.String(200), nullable = False)

class GoogleTrend(db.Model):
        __tablename__ = "googletrend"
        date = db.Column("date", db.Date(), nullable = False, primary_key=True)
        terrorism = db.Column("terrorism",db.Integer(), nullable = False)
        terrorist_attack = db.Column("terrorist_attack",db.Integer(), nullable = False)
        terror_attack = db.Column("terror_attack",db.Integer(), nullable = False)
        terrorism_act = db.Column("terrorism_act",db.Integer(), nullable = False)
        weighted_avg = db.Column('weighted_avg', db.Numeric(), nullable = False)
        year = db.Column('year', db.Integer(), nullable = False)
        month = db.Column('month', db.Integer(), nullable = False)