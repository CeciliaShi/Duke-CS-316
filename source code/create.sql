CREATE TABLE Incident
(id BIGINT NOT NULL PRIMARY KEY,
 date DATE,
 international INT,
 property_damage INT,
 nwound INT,
 nkill INT,
 CHECK (international IN (0,1)),
 CHECK (property_damage IN (0,1)),
 CHECK (id<1000000000000 AND id>= 197000000001),
 CHECK (nwound >=0 OR nwound IS NULL),
 CHECK (nkill >= 0 OR nkill IS NULL)
 );


CREATE TABLE Location
(latitude NUMERIC NOT NULL CHECK(latitude <= 90 AND latitude >= -90), 
 longitude NUMERIC NOT NULL CHECK(longitude <= 180 AND longitude >= -180),
 country VARCHAR(256),
 prov_state VARCHAR(256),
 city VARCHAR(256),
 PRIMARY KEY(latitude,longitude)
 );



CREATE TABLE Happened
(latitude NUMERIC NOT NULL, 
 longitude NUMERIC NOT NULL ,
 incident_id BIGINT NOT NULL, 
 PRIMARY KEY(incident_id),
 FOREIGN KEY(latitude,longitude) REFERENCES Location(latitude,longitude),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
 );



CREATE TABLE InitiatedBy 
(perpetrator_name VARCHAR(256) NOT NULL,
 incident_id BIGINT NOT NULL PRIMARY KEY, 
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
 );



CREATE TABLE Used
(incident_id BIGINT NOT NULL PRIMARY KEY, 
 weapon_type VARCHAR(256) NOT NULL,
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
);



CREATE TABLE BelongedTo
(incident_id BIGINT NOT NULL PRIMARY KEY, 
 attack_type VARCHAR(256) NOT NULL,
 succussful_attack INT NOT NULL,
 suicide_attack INT NOT NULL,
 FOREIGN KEY(incident_id) REFERENCES Incident(id),
 CHECK (succussful_attack IN (0,1)),
 CHECK (suicide_attack IN (0,1))
 );



CREATE TABLE Targeted
(incident_id BIGINT NOT NULL PRIMARY KEY,
 victim_type VARCHAR(256) NOT NULL,
 subtype VARCHAR(256) NOT NULL,
 target VARCHAR(256) NOT NULL,
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
);

CREATE TABLE Comment
(user_id SERIAL NOT NULL PRIMARY KEY,
 name VARCHAR(20) NOT NULL,
 message VARCHAR(200) NOT NULL
);


--- CREATE A SAMPLE DATABASE
--- INSERT DATA 

INSERT INTO Incident(id, date, international, property_damage, nwound, nkill) VALUES
(197000000001, '1970-07-02', 0, 0, 0, 1),
(197003240002, '1970-03-24', 1, 0, 0, 0),
(197001050001, '1970-01-01', -9, 1, 0, 0)
;

INSERT INTO Location VALUES
(18.456792, -69.951164, 'Dominican Republic', NULL, 'Santo Domingo'),
--(18.456792, -69.951164, 'Dominican Republic', NULL, 'Santo Domingo'),
(43.46850, -89.744299, 'United States', 'Wisconsin', 'Baraboo')
;

INSERT INTO Targeted(incident_id, victim_type) VALUES
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

INSERT INTO Comment(name, message) VALUES
('Mike', 'We hope for a peaceful world!'),
('Ben', 'I feel sorry for those who went through any of these horrible event.'),
('Alice', 'We need to learn to protect ourselves and our beloved ones.');

--- VALIDATE THE DESIGN
--- THESE SHOULD NOT BE SUCCESSFULLY INSERTED INTO THE TABLE

--- THIS CREATES DUPLICATES AND VIOLATES THE KEY CONSTRAINT
INSERT INTO Location VALUES
(18.456792, -69.951164, 'Dominican Republic', NULL, 'Santo Domingo');

--- THIS VIOLATES THE CHECK OF INTERNATIONAL FOR THE TABLE INCIDENT
INSERT INTO Incident(id, date, international, property_damage, nwound, nkill) VALUES
(197001000002, '1970-07-01', 10, 0, 0, 1);

--- THIS VIOLATES THE REFERNTIAL INTEGRITY
INSERT INTO Used(incident_id,weapon_type) VALUES
(0000000001, 'Unknown');

--- THIS VIOLATES THE CHECK FOR LATITUDE IN THE TABLE LOCATION
INSERT INTO Location VALUES
(190.01, -195.12, NULL, NULL, NULL);



