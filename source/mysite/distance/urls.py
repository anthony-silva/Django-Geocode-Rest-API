from django.urls import path
from . import views

app_name = 'distance'
urlpatterns = [
    # ex: /results/
    path('', views.IndexView, name='index'),
    path('results/', views.ResultsView, name='results')
]