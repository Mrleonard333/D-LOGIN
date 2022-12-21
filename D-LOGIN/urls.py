from django.urls import path
from . import views

urlpatterns = [ # < Urls of the app
    path('', views.index, name='Home'),
    path('SING_UP/', views.SING_UP, name='SING_UP'),
    path('LOGIN/', views.LOGIN, name='LOGIN')
]