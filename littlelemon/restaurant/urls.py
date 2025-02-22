from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # Frontend URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('book/', views.book_view, name='book'),
    path('bookings/', views.bookings, name='bookings'),
    path('reservations/', views.reservations, name='reservations'),
    
    # API endpoints
    path('api/', views.api_root),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('api/menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
    path('api/categories/', views.CategoryView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', views.SingleCategoryView.as_view(), name='category-detail'),
    path('api/bookings/', views.BookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='booking-list'),
    path('api/bookings/<int:pk>/', views.BookingViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='booking-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
