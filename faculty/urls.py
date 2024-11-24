from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='faculty-homepage'),
    path('files/', views.files, name='faculty-files'),
    path('generalSubmissionBin/', views.submissionBinList, name='submission-bin-list'),
    path('generalSubmissionBin/submit-document/<int:submission_bin_id>/', views.submit_document, name='submit_document'),
    path('notifications/', views.faculty_notification_list, name='faculty-notifications'),
    path('notifications/mark-as-rad/<int:notification_id>/', views.mark_as_read, name='mark-as-read'),
    path('notifications/count', views.unread_notification_count, name='unread-notification-count')
]