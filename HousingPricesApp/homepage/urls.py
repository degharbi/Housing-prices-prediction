from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.post),
    path('dashboard.html', views.test),
    path('Gradient_Boosting.html', views.test2),
]

