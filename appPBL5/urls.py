from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('manager', views.homeManager, name='manager'),
    path('details/<int:id>', views.details, name='details'),
]