from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.list_users, name='list_users'),      # List all users
    path('users/new/', views.create_user, name='create_user'), # Create a new user
    path('users/<int:pk>/edit/', views.update_user, name='update_user'),  # Update a user
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'), # Delete a user
]
