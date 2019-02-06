from django.urls import path

from . import views

app_name = 'ride'

urlpatterns = [
    path('', views.home, name='home'),
    path('requests/', views.ViewRequests.as_view(), name='view_requests'),
    path('new-request/', views.request_new, name='request_new'),
    path('owner/request-detail/<int:pk>/', views.OwnerRequestDetailView.as_view(), name='owner_request_detail'),
    path('sharer/request-detail/<int:pk>/', views.MySharerRequestDetailView.as_view(), name='sharer_request_detail'),
    path('owner-request-edit/<int:pk>/', views.OwnerRequestEditView.as_view(), name='owner_request_edit'),
    #path('sharer-request-edit/', views.SharerRequestEditView.as_view(), name='sharer_request_edit'),
    path('driver/', views.driver_home, name='driver_home'),
    path('driver/registration/', views.driver_registration, name='driver_registration'),
    path('driver/view-requests/', views.driver_view_requests, name='driver_view_requests'),
    path('driver/view-requests/<int:pk>/', views.driver_request_detail, name='driver_request_detail'),
    path('sharer/search-ride/', views.sharer_search_ride, name='sharer_search_ride'),
    path('sharer/owner-request-detail/<int:pk>/<int:passenger_num>/',  views.SharerOwnerRequestDetailView.as_view(), name='sharer_ownerrequest_detail'),
    path('sharer/join/<int:owner_request_id>/<int:passenger_num>/', views.sharer_join, name='sharer_join'),
]