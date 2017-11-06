\COPY Incident(id, international, property_damage, nwound, nkill, date) FROM 'data/Incident.csv' WITH DELIMITER ',' NULL '' CSV 
\COPY Location(latitude, longitude, country, prov_state, city) FROM 'data/Location.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Happened(incident_id, latitude, longitude) FROM 'data/Happened.csv' WITH DELIMITER ',' NULL '' CSV
\COPY InitiatedBy(incident_id, perpetrator_name) FROM 'data/InitiatedBy.csv' WITH DELIMITER ',' NULL '' CSV 
\COPY Used(incident_id, weapon_type) FROM 'data/Used.csv' WITH DELIMITER ',' NULL '' CSV
\COPY BelongedTo(incident_id, attack_type, succussful_attack, suicide_attack) FROM 'data/BelongedTo.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Targeted(incident_id, victim_type, subtype, target) FROM 'data/Targeted.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Comment(user_id, name, message) FROM 'data/Comment' WITH DELIMITER ',' NULL '' CSV