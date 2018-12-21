from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage),
    path('dashboard.html', views.dashboard),
    path('Gradient_Boosting.html', views.notebook),
]

