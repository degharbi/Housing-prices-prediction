#!/bin/bash

# Load CSV file 
echo 'Enter CSV file path to load into ElasticSearch' ; read Csvfile

# Elastic Search parameters
echo 'Enter your ip adress (ex: localhost)' ; read ip ;
echo 'Enter your port (ex: 9200)' ; read port
echo 'Enter elastic search index (ex: myindex)' ; read index
echo 'Enter elastic search type (ex: mytype)' ; read type

echo 'http://'$ip':'$port'/'$index'/'$type
