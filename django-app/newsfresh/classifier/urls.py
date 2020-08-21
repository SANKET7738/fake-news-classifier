from django.urls import path
from . import views

app_name = 'classifier'

urlpatterns = [
    path('', views.index, name='index'),
    path('form/',views.form, name='form'),
    path('output/',views.output, name='output')
    

]