from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login),
    path('register', views.register),
    path('succeed', views.succeed),
    path('failed', views.failed),
    path('show', views.show),
    path('delete/<int:id>', views.delete),
]