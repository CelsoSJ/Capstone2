from django.urls import path
from . import views



urlpatterns = [
  path('userManagement/', views.userManagement, name='userManagement'),
  path('homepage/', views.home_page, name='dean-homepage'),
  path('userManagement/create_user/', views.create_user, name='create_user'),
  path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('files/', views.department_files_view, name='department-files'),
  path('archive-user/<int:user_id>/', views.archive_user, name='archive-user'),
  path('list-of-archived-users/', views.list_of_archived_user, name='list-of-archived-users'),
  path('list-of-archived-users/delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
  path('list-of-archived-users/restore-user/<int:user_id>/', views.restore_user, name='restore-user')
]