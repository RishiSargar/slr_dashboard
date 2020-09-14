QUERY_HOURLY = """
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ",CAST(EXTRACT(hour from t1) as string),":00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 24
"""
QUERY_DAILY="""
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ","00:00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 7
"""
QUERY_WEEKLY="""
SELECT controller_id,TIMESTAMP (CONCAT(CAST(DATE as STRING)," ","00:00:00")) as hour_number, Avg(temperature) as Average_temp,Avg(ph) as Average_ph,Avg(ec) as Average_ec
from (select controller_id,DATE(timestamp, "America/Phoenix") as DATE,DATETIME(timestamp, "America/Phoenix") as t1,temperature,ph,ec
FROM `ninth-tensor-233119.cc_dataset.sensor_data` where controller_id='{}'
)GROUP BY hour_number, controller_id, DATE
order by DATE desc , hour_number desc limit 7