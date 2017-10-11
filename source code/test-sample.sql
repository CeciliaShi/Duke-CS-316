-- selection option: user inputs location and time, time series trend in the given time and location will be generated
SELECT international, property_damage, nwound, nkill
FROM Incident, Location
WHERE datetime <= '1970-07-02' AND 
datetime >= '1970-03-24' AND 
country = 'Dominican Republic';


-- selection option: user inputs date and location, attack type pie chart will be generated
CREATE VIEW AttackType AS 
SELECT BelongedTo.attack_type, COUNT(*) AS count
FROM Incident, Location, BelongedTo
WHERE Incident.id = BelongedTo.incident_id AND 
datetime <= '1970-07-02' AND 
datetime >= '1970-03-24' AND 
country = 'Dominican Republic' 
GROUP BY BelongedTo.attack_type;

CREATE VIEW Total AS
SELECT SUM(count) as total
FROM AttackType;

SELECT attack_type, count/Total AS perc
FROM AttackType, Total;