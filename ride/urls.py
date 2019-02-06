from django.urls import path

from . import views

app_name = 'ride'

urlpatterns = [
    path('', views.home, name='home'),
    path('requests/', views.ViewRequests.as_view(), name='view_requests'),
    path('new-request/', views.request_new, name='request_new'),
    path('owner/request-detail/<int:pk>/', views.OwnerRequestDetailView.as_view(), name='owner_request_detail'),
    path('sharer/request-detail/<int:pk>/', views.SharerRequestDetailView.as_view(), name='sharer_request_detail'),
    path('owner-request-edit/<int:pk>/', views.OwnerRequestEditView.as_view(), name='owner_request_edit'),
    path('sharer-request-edit/', views.SharerRequestEditView.as_view(), name='sharer_request_edit'),
    path('driver/', views.driver_home, name='driver_home'),
    path('driver/registration/', views.driver_registration, name='driver_registration'),
    path('driver/view-requests/', views.driver_view_requests, name='driver_view_requests'),
    path('driver/view-requests/<int:pk>/', views.driver_request_detail, name='driver_request_detail'),
    path('sharer/owner-request-detail/<int:pk>/', views.sharer_ownerrequest_detail, name='sharer_ownerrequest_detail'),
    path('new-share-request/', views.sharer_request_search, name='sharer_request_search'),
]