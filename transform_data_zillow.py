#!/usr/bin/env python
# coding: utf-8

# In[50]:


get_ipython().system('pip install PyGithub')


# In[9]:


get_ipython().system('pip install pprint')


# In[126]:


import json
import numpy as np
from pprint import pprint
with open('Housing-prices-prediction/data/not_sold.json') as f:
    data = json.loads(f.read())


# In[127]:


properties = [property[8][11] for property in data['map']['properties']]


# In[128]:


from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')


# In[200]:


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
    producer.send('data_new', str(message))


# In[206]:


from kafka import KafkaConsumer
consumer = KafkaConsumer('data_new', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')


# In[202]:


from github import Github
g = Github("8afa3797fac223c9b4682a76127aeb6e3d191189")
repo = g.get_repo("degharbi/Housing-prices-prediction")


# In[ ]:


data_new = 'id,date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,vue,condition,    grade,sqft_above,sqft_basement,yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15'+'\n'
#repo.create_file("data/data_new3.csv", "test", msg, branch="master")


# In[196]:


contents = repo.get_contents("data/data_new.csv")


# In[207]:


for msg in consumer:
    msg = msg.value.replace("[","").replace("]","")
    print(msg)
    data_new = data_new+str(msg)+'\n'


# In[208]:


contents = repo.get_contents("data/data_new.csv")
repo.update_file(contents.path, 'test',data_new, contents.sha, branch="master")

