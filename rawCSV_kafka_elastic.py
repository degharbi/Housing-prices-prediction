#!/usr/bin/env python
# coding: utf-8

from kafka import KafkaProducer
from kafka import KafkaConsumer
import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

consumer = KafkaConsumer('data_raw', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
es = Elasticsearch()
es.indices.create(index='properties', ignore=400)

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
