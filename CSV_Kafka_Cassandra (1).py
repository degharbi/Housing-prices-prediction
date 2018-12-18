#!/usr/bin/env python
# coding: utf-8

# In[2]:


from kafka import KafkaProducer
import requests


# In[3]:


producer = KafkaProducer(bootstrap_servers='localhost:9092')


# In[4]:


url = 'https://raw.githubusercontent.com/degharbi/Housing-prices-prediction/master/data/kc_house_data.csv'

data_csv = requests.get(url).content


# In[5]:


messages = [line.replace('\n','') for line in data_csv.split('\n')[1:]]


# In[6]:


for message in messages:
    producer.send('data_raw', message)


# In[8]:


from kafka import KafkaConsumer


# In[7]:


get_ipython().system(u'pip install cassandra-driver')


# In[9]:


from cassandra.cluster import Cluster

cluster = Cluster()


# In[10]:


session = cluster.connect()


# In[10]:


session.execute(
    """
    CREATE KEYSPACE IF NOT EXISTS 
    housing_prices 
    WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}
    """
)


# In[11]:


session.execute(
    """
    CREATE TABLE IF NOT EXISTS housing_prices.properties2(
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


# In[36]:


consumer = KafkaConsumer('data_raw', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')


# In[37]:


for msg in consumer :
    msg = msg.value.replace("'","").split(',')
    print(msg)
    session.execute(
        """
        INSERT INTO housing_prices.properties2 (
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


# In[13]:


get_ipython().system(u'pip install elasticsearch')


# In[24]:


from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
es = Elasticsearch()


# In[23]:


es.indices.create(index='properties', ignore=400)


# In[33]:


es.indices.create(index='properties', ignore=400)


# In[38]:


def gendata(consumer):
    for msg in consumer:
        msg = msg.value.replace("'","").split(',')
        yield {
            "_index": "properties",
            "_type": "document",
            "doc": {
                "id": msg[0],
                "date": msg[1],
                "price": float(msg[2]),
                "bedrooms": int(msg[3]),
                "bathrooms": float(msg[4]),
                "sqft_living": int(msg[5]),
                "sqft_lot": int(msg[6]),
                "floors": float(msg[7]),
                "waterfront": int(msg[8]),
                "vue": int(msg[9]),
                "condition": int(msg[10]),
                "grade": int(msg[11]),
                "sqft_above": int(msg[12]),
                "sqft_basement": int(msg[13]),
                "yr_built": int(msg[14]),
                "yr_renovated": int(msg[15]),
                "zipcode": int(msg[16]),
                "lat": float(msg[17]),
                "long": float(msg[18]),
                "sqft_living15": int(msg[19]),
                "sqft_lot15": int(msg[20])                         
            }
        }

bulk(es, gendata(consumer))
