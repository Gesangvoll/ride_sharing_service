from django.urls import path

from . import views

app_name = 'ride'

urlpatterns = [
    path('', views.home, name='home'),
    path('requests/', views.ViewRequests.as_view, name='view_requests'),
    path('new-request/', views.request_new, name='request_new'),
    path('driver/', views.driver_home, name='driver_home'),
    path('new-share-request/', views.sharer_request_new, name='sharer_request_new'),
]