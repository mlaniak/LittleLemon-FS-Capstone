from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # API root
    path('', views.api_root),
    
    # User endpoints
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    
    # Menu endpoints
    path('menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items-list'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-items-detail'),
    
    # Authentication endpoints
    path('message/', views.msg, name='protected-message'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
