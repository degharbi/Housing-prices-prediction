#!/usr/bin/env python
# coding: utf-8

from kafka import KafkaProducer
from kafka import KafkaConsumer
import requests
from cassandra.cluster import Cluster

producer = KafkaProducer(bootstrap_servers='localhost:9092')
url = 'https://raw.githubusercontent.com/degharbi/Housing-prices-prediction/master/data/kc_house_data.csv'
data_csv = requests.get(url).content
messages = [line.replace('\n','') for line in data_csv.split('\n')[1:]]

# Send each line from the csv into a message with a topic data_raw
for message in messages:
    producer.send('data_raw', message)

# Initiqte a cluster and a cassandra connection
cluster = Cluster()
session = cluster.connect()

# Create keyspace in cassandra
session.execute(
    """
    CREATE KEYSPACE IF NOT EXISTS 
    housing_prices 
    WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}
    """
)

# Create a table inside the keyspace
session.execute(
    """
    CREATE TABLE IF NOT EXISTS housing_prices.properties(
     id TEXT,
     date TEXT,
     price FLOAT,
     bedrooms INT,
     bathrooms FLOAT,
     sqft_living INT,
     sqft_lot INT,
     floors FLOAT,
     waterfront INT,
     vue INT,
     condition INT,
     grade INT,
     sqft_above INT,
     sqft_basement INT,
     yr_built INT,
     yr_renovated INT,
     zipcode INT,
     lat FLOAT,
     long FLOAT,
     sqft_living15 INT,
     sqft_lot15 INT,
    PRIMARY KEY (id))
    """
)

# Consume the messages prodeces in the topic data_raw
consumer = KafkaConsumer('data_raw', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

# Save these messages into our cassandra table
for msg in consumer :
    msg = msg.value.replace("'","").split(',')
    print(msg)
    session.execute(
        """
        INSERT INTO housing_prices.properties (
             id,
             date,
             price,
             bedrooms,
             bathrooms,
             sqft_living,
             sqft_lot,
             floors,
             waterfront,
             vue,
             condition,
             grade,
             sqft_above,
             sqft_basement,
             yr_built,
             yr_renovated,
             zipcode,
             lat,
             long,
             sqft_living15,
             sqft_lot15
         )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s)
        """,
        (
            msg[0],
            msg[1],
            float(msg[2]),
            int(msg[3]),
            float(msg[4]),
            int(msg[5]),
            int(msg[6]),
            float(msg[7]),
            int(msg[8]),
            int(msg[9]),
            int(msg[10]),
            int(msg[11]),
            int(msg[12]),
            int(msg[13]),
            int(msg[14]),
            int(msg[15]),
            int(msg[16]),
            float(msg[17]),
            float(msg[18]),
            int(msg[19]),
            int(msg[20]),
        )
    ) 
