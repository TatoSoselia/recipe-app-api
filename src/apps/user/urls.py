"""
Url mappings for the users API.
"""
from django.urls import path
from apps.user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
