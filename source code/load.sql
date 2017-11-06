\COPY Incident(id, date, international, property_damage, nwound, nkill) FROM 'data/Incident.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY Location(latitude, longitude, country, prov_state, city) FROM 'data/Location.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY Happened(latitude, longitude, incident_id) FROM 'data/Happened.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY InitiatedBy(incident_id, perpetrator_name) FROM 'data/InitiatedBy.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY Used(incident_id, weapon_type) FROM 'data/Used.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY BelongedTo(incident_id, attack_type, succussful_attack, suicide_attack) FROM 'data/BelongedTo.csv' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY Targeted(incident_id, victime_type, subtype, target) FROM 'data/Targeted' WITH DELIMITER ',' NULL '' CSV HEADER 
\COPY Comment(user_id, name, message) FROM 'data/Comment' WITH DELIMITER ',' NULL '' CSV HEADER 
