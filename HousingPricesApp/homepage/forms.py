from django import forms

class Searchform(forms.Form):
	bedrooms = forms.FloatField(label='bedrooms', required=True, initial=3)
	sqft_living = forms.FloatField(label='sqft_living', required=True, initial=1180)
	sqft_lot = forms.FloatField(label='sqft_lot', required=True, initial=5650)
	lat = forms.FloatField(label='latitude', required=True, initial=47.5112)
	longi = forms.FloatField(label='longitude', required=True, initial=-122.257	)	