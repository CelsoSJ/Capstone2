from django.urls import path
from . import views



urlpatterns = [
  path('userManagement/', views.userManagement, name='userManagement'),
  path('homepage/', views.home_page, name='dean-homepage'),
  path('userManagement/create_user/', views.create_user, name='create_user'),
  path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate')
]