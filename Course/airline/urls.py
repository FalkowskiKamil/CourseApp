from django.urls import path
from . import views

app_name = 'airline'
urlpatterns=[
    path('', views.index, name='airline_index'),
    path('passager/<int:passager_id>', views.passager, name='passager'),
]