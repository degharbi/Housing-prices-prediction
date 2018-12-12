#!/bin/bash
file=`pwd`'/kc_house_data.csv'
while read f1
do
   curl -XPOST 'http://localhost:9200/housing_prices/properties' -H "Content-Type: application/json" -u elastic:secret -d "{ \"properties\": \"$f1\" }"
done < $file
