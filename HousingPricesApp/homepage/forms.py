from django import forms

class Searchform(forms.Form):
	feature1  = forms.FloatField(label='sqft_living', required=False)	
	feature2  = forms.FloatField(label='sqft_lot', required=False)
	feature3  = forms.FloatField(label='latitude', required=False)
	feature4  = forms.FloatField(label='longitude', required=False)
	
	