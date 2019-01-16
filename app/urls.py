from django.urls import path
from app import views


urlpatterns = [
    path('', views.basic, name='basic'),
    path('prediction', views.prediction, name='prediction')
]
