CREATE TABLE Incident
(id BIGINT NOT NULL PRIMARY KEY,
 datetime DATE NOT NULL,
 international INT NOT NULL,
 property_damage INT NOT NULL,
 nwound INT,
 nkill INT,
 CHECK(international IN (0,1,-9) AND property_damage IN (0,1,-9)),
 CHECK (id<1000000000000)
 );


CREATE TABLE Location
(latitude NUMERIC NOT NULL, 
 longitude NUMERIC NOT NULL ,
 country VARCHAR(256),
 prov_state VARCHAR(256),
 city VARCHAR(256),
 PRIMARY KEY(latitude,longitude)
 );



CREATE TABLE Happened
(latitude NUMERIC NOT NULL, 
 longitude NUMERIC NOT NULL ,
 incident_id BIGINT NOT NULL, 
 PRIMARY KEY(latitude,longitude,incident_id),
 FOREIGN KEY(latitude,longitude) REFERENCES Location(latitude,longitude),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
 );



CREATE TABLE InitiatedBy 
(perpetrator_name VARCHAR(256) NOT NULL,
 incident_id BIGINT NOT NULL, 
 PRIMARY KEY(perpetrator_name,incident_id),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
 );



CREATE TABLE Used
(incident_id BIGINT NOT NULL, 
 weapon_type VARCHAR(256) NOT NULL,
 PRIMARY KEY(incident_id,weapon_type),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
);




CREATE TABLE BelongedTo
(incident_id BIGINT NOT NULL, 
 attack_type VARCHAR(256) NOT NULL,
 succussful_attack INT NOT NULL,
 suicide_attack INT NOT NULL,
 PRIMARY KEY(incident_id,attack_type,succussful_attack,suicide_attack),
 FOREIGN KEY(incident_id) REFERENCES Incident(id),
 CHECK (succussful_attack IN (0,1) AND suicide_attack IN (0,1))
 );



CREATE TABLE Targeted
(incident_id BIGINT NOT NULL,
 victime_type VARCHAR(256) NOT NULL,
 PRIMARY KEY(incident_id,victime_type),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
);




---INSERT DATA

INSERT INTO Incident(id, datetime, international, property_damage, nwound, nkill) VALUES
(197000000001, '1970-07-02', 0, 0, 0, 1),
(197003240002, '1970-03-24', 1, 0, 0, 0),
(197001050001, '1970-01-01', -9, 1, 0, 0)
;

INSERT INTO Location VALUES
(18.456792, -69.951164, 'Dominican Republic', NULL, 'Santo Domingo'),
--(18.456792, -69.951164, 'Dominican Republic', NULL, 'Santo Domingo'),
(43.46850, -89.744299, 'United States', 'Wisconsin', 'Baraboo')
;

INSERT INTO Targeted(incident_id, victime_type) VALUES
  (197000000001, 'Private Citizens & Property'),
  (197003240002, 'Military'),
  (197001050001,'Military')
  ;


INSERT INTO BelongedTo(incident_id,attack_type,succussful_attack,suicide_attack) VALUES
  (197000000001, 'Assassination',1,0),
  (197003240002, 'Hostage Taking (Kidnapping)', 1, 0),
  (197001050001, 'Bombing/Explosion', 0, 0)
  ;


INSERT INTO Used(incident_id,weapon_type) VALUES
  (197000000001, 'Unknown'),
  (197003240002, 'Unknown'),
  (197001050001, 'Explosives/Bombs/Dynamite')
  ;



INSERT INTO InitiatedBy(perpetrator_name,incident_id) VALUES
  ('MANO-D',197000000001),
  ('Dominican Popular Movement (MPD)', 197003240002),
  ('Weather Underground, Weathermen',197001050001)
  ;


INSERT INTO Happened(latitude,longitude,incident_id) VALUES
  (18.456792, -69.951164,197000000001),
  (18.456792, -69.951164, 197003240002),
  (43.46850, -89.744299,197001050001)
  ;
