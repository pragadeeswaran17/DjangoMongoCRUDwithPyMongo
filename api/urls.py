from django.urls import path
from api import views

urlpatterns = [
    path("home/", views.home ),
    path("add/", views.addUser),
    path("users/", views.users),
    path("user/<str:name>/", views.user),
    
    
]

""" path("user/<str:user_id>/", views.user) """