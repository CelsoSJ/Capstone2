from django.urls import path
from . import views

urlpatterns = [
  path('', views.home_page, name='qao-homepage'),
  path('files', views.all_files, name='all-approved-files')
]