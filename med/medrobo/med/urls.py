from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from . import views
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'add',views.add,name='add'),
	url(r'show',views.show,name='show'),
	url(r'results',views.results,name='results'),
	url(r'delete_data',views.delete_data,name='delete_data')
    
]
