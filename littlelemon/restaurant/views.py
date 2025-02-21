from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Menu, Booking
from .serializers import MenuItemSerializer, UserSerializer, BookingSerializer

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'menu': reverse('menu-list', request=request)
    })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MenuItemsView(generics.ListCreateAPIView):
    """API endpoint for listing and creating menu items.
    GET: List all menu items (public)
    POST: Create a new menu item (requires authentication)
    """
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        # Allow read access to all users, but require authentication for create
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting individual menu items.
    GET: Retrieve a menu item (public)
    PUT/PATCH: Update a menu item (requires authentication)
    DELETE: Remove a menu item (requires authentication)
    """
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        # Allow read access to all users, but require authentication for update/delete
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookingViewSet(viewsets.ModelViewSet):
    """API ViewSet for managing restaurant bookings.
    
    Provides CRUD operations:
    - list: Get all bookings (requires authentication)
    - create: Create a new booking (requires authentication)
    - retrieve: Get a specific booking (requires authentication)
    - update: Update a booking (requires authentication)
    - delete: Remove a booking (requires authentication)
    
    All operations require authentication to protect customer data.
    """
    queryset = Booking.objects.all().order_by('bookingdate')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return bookings ordered by date.
        Can be extended to filter by user, date range, etc.
        """
        return super().get_queryset()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def msg(request):
    return Response({"message": "This view is protected"})
