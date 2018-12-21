from django.shortcuts import render, redirect	
from homepage.forms import Searchform 

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import locale
locale.setlocale( locale.LC_ALL, '' )

def homepage(request):
	if request.method == 'POST':	
		form = Searchform(request.POST)
		if form.is_valid():
			sqft_living = form.cleaned_data['sqft_living']
			sqft_lot = form.cleaned_data['sqft_lot']
			bedrooms = form.cleaned_data['bedrooms']
			lat = form.cleaned_data['lat']
			longi = form.cleaned_data['longi']
	else:
		bedrooms= 3
		sqft_living= 1180
		sqft_lot = 5650
		lat= 47.5112
		longi= -122.257		
		form = Searchform()
	
	raw = pd.read_csv('https://raw.githubusercontent.com/degharbi/Housing-prices-prediction/master/data/kc_house_data.csv')
	data = {
		'sqft_living': raw['sqft_living'].values,
		'sqft_lot': raw['sqft_lot'].values,
		'bedrooms': raw['bedrooms'].values,
		'lat': raw['lat'].values,
		'long': raw['long'].values		
	}

	X = pd.DataFrame(
		data=data,
		index=raw['id'].values, 
	)
	y = raw.price.values
	x = X
	X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.33, random_state=0)

	model = Pipeline([('poly', PolynomialFeatures(degree=2)),
					('linear', LinearRegression(fit_intercept=False))])

	reg = model.fit(X_train, y_train)

	to_predict = [[
		sqft_living,
		sqft_lot,
		bedrooms,
		lat,
		longi,
	]]
	 
	predicted = locale.currency( 
		reg.predict(to_predict)[0], 
		grouping=True 
		)
 
	args = {
		'form': form,
		'predicted': predicted,
		'test_score' : reg.score(X_test, y_test),
		'lat' : lat,
		'long' : longi,
		}
	return render(request, 'homepage/page_accueil.html', args)

def dashboard(request):
 
	args = {
		}
	return render(request, 'homepage/dashboard.html', args)

def notebook(request):
	return render(request, 'homepage/Gradient_Boosting.html')
