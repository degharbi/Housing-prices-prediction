from django.shortcuts import render, redirect	
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from homepage.forms import Searchform 
from bs4 import BeautifulSoup
import requests, sqlite3
import json
from datetime import datetime
from re import compile

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.utils import check_random_state
from sklearn.model_selection import train_test_split

def post(request):
	if request.method == 'POST':	
		form = Searchform(request.POST)
		if form.is_valid():
			feature1 = form.cleaned_data['feature1']			
			feature2 = form.cleaned_data['feature2']			
			feature3 = form.cleaned_data['feature3']			
			feature4 = form.cleaned_data['feature4']			
	else:
		feature1, feature2, feature3, feature4 = 0, 0, 0, 0
		form = Searchform()
	
	raw = pd.read_csv('kc_house_data.csv')
	data = {
		'sqft_living': raw['sqft_living'].values,
		'sqft_lot': raw['sqft_lot'].values,
		'lat': raw['lat'].values,
		'long': raw['long'].values,
	}

	X = pd.DataFrame(
		data=data,
		index=raw['id'].values, 
	)
	y = raw.price.values
	x = X
	X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.33, random_state=0)

	lr = LinearRegression().fit(X_train, y_train)

	train_score = lr.score(X_train, y_train)
	test_score = lr.score(X_test, y_test)

	to_predict = [[feature1, feature2, feature3, feature4]]
	predicted = int(lr.predict(to_predict)[0]) 
 
	args = {
		'form': form,
		'resultat': predicted,
		'train_score': train_score,
		'test_score' : test_score,
		'lat' : feature3,
		'long' : feature4,
		}
	return render(request, 'homepage/page_accueil.html', args)

def test(request):
 
	args = {
		}
	return render(request, 'homepage/dashboard.html', args)

def test2(request):
 
	args = {
		}
	return render(request, 'homepage/test2.html', args)
