CREATE TABLE Incident
(id BIGINT NOT NULL PRIMARY KEY,
 international INT NOT NULL,
 property_damage INT NOT NULL,
 nwound INT,
 nkill INT,
 date DATE,
 CHECK (international IN (0,1,-9)),
 CHECK (property_damage IN (0,1,-9)),
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
(incident_id BIGINT NOT NULL,
 latitude NUMERIC NOT NULL, 
 longitude NUMERIC NOT NULL , 
 PRIMARY KEY(incident_id),
 FOREIGN KEY(latitude,longitude) REFERENCES Location(latitude,longitude),
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
 );



CREATE TABLE InitiatedBy 
(incident_id BIGINT NOT NULL PRIMARY KEY, 
 perpetrator_name VARCHAR(256) NOT NULL,
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
 target VARCHAR(500) NOT NULL,
 FOREIGN KEY(incident_id) REFERENCES Incident(id)
);

CREATE TABLE Comment
(user_id SERIAL NOT NULL PRIMARY KEY,
 name VARCHAR(20) NOT NULL,
 message VARCHAR(200) NOT NULL
);

