from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('manager', views.homeManager, name='manager'),
    path('user', views.homeUser, name='user'),
    path('details/<int:id>', views.details, name='details'),
    path('createuser', views.createuser, name='createuser'),
    path('user_update/<int:user_id>/', views.user_update, name='user_update'),
    path('user_delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('parking_history', views.parking_history, name='parking_history'),
    path('logout', views.logout, name='logout'),
    path('update_user', views.update_user, name='update_user'),
    path('parking_history_user', views.parking_history_user, name='parking_history_user'),
]