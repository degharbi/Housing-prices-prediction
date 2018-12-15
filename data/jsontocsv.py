import json
import numpy as np
from pprint import pprint
with open('Housing-prices-prediction/data/not_sold.json') as f:
    data = json.loads(f.read())

properties = [property[8][11] for property in data['map']['properties']]
for property in properties:
    id= np.random.random_integers(0000000001, high=9999999999)
    date = ''
    price= ''
    try: bedrooms= property['bedrooms']
    except: pass
    try: bathrooms = property['bathrooms']
    except: pass
    try: sqft_living = property['livingArea']
    except: pass
    try: sqft_lot = property['lotSize']
    except: pass
    try: floors= ''
    except: pass
    try: waterfront= ''
    except: pass
    vue= ''
    condition= ''
    grade=''
    sqft_above= ''
    sqft_basement= ''
    try:yr_built = property['yearBuilt']
    except: pass
    yr_renovated= ''
    try:zipcode= property['zipcode']
    except: pass
    try:lat = property['latitude']*10
    except: pass
    try:long= property['longitude']
    except: pass
    sqft_living15= ''
    sqft_lot15= ''
    
    message = [
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
         sqft_lot15,
    ]
