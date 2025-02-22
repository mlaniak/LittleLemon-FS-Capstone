from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Menu, Booking, Category
from .serializers import MenuItemSerializer, UserSerializer, BookingSerializer, CategorySerializer
import json

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'menu': reverse('menu-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'bookings': reverse('booking-list', request=request, format=format),
    })

def home(request):
    context = {
        'special_offer': {
            'title': 'SPECIAL OFFER',
            'description': '30% Off This Weekend',
            'discount': 30,
        },
        'menu_items': Menu.objects.all()[:3],  # Get latest 3 menu items
        'opening_hours': {
            'weekdays': '2pm - 10pm',
            'saturday': '2pm - 11pm',
            'sunday': '2pm - 9pm'
        }
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def menu_view(request):
    categories = Category.objects.prefetch_related('menu_items').all()
    return render(request, 'menu.html', {'categories': categories})

def book_view(request):
    return render(request, 'book.html')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def bookings(request):
    # Define all available time slots
    ALL_TIME_SLOTS = [
        "10:00", "11:00", "12:00", "13:00", "14:00", 
        "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"
    ]

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['first_name', 'reservation_date', 'reservation_slot']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return JsonResponse({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }, status=400)
            
            # Validate and sanitize name
            name = data['first_name'].strip()
            if not name:
                return JsonResponse({'error': 'Name cannot be empty'}, status=400)
            if not all(c.isalpha() or c.isspace() for c in name):
                return JsonResponse({'error': 'Name can only contain letters and spaces'}, status=400)
            
            # Validate and parse date
            try:
                date = datetime.strptime(data['reservation_date'], '%Y-%m-%d').date()
                today = datetime.now().date()
                
                if date < today:
                    return JsonResponse({'error': 'Cannot make reservations for past dates'}, status=400)
                
                # Optional: Limit advance bookings to e.g., 30 days
                max_date = today + timedelta(days=30)
                if date > max_date:
                    return JsonResponse({
                        'error': 'Reservations can only be made up to 30 days in advance'
                    }, status=400)
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            # Validate time slot
            slot = data['reservation_slot']
            if slot not in ALL_TIME_SLOTS:
                return JsonResponse({'error': 'Invalid time slot selected'}, status=400)
            
            # Check if slot is already booked
            existing_booking = Booking.objects.filter(
                reservation_date=date,
                reservation_slot=slot
            ).first()
            
            if existing_booking:
                return JsonResponse({
                    'error': 'This time slot is already booked'
                }, status=400)
            
            # Create new booking
            try:
                booking = Booking.objects.create(
                    first_name=name,
                    reservation_date=date,
                    reservation_slot=slot
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Booking confirmed successfully'
                })
            except Exception as e:
                return JsonResponse({
                    'error': 'Failed to save booking. Please try again.'
                }, status=500)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    elif request.method == 'GET':
        # Check if this is an API request (has date parameter)
        date_param = request.GET.get('date')
        if date_param:
            try:
                date = datetime.strptime(date_param, '%Y-%m-%d').date()
                today = datetime.now().date()
                
                if date < today:
                    return JsonResponse({
                        'error': 'Cannot view bookings for past dates',
                        'available_slots': [],
                        'bookings': []
                    })
                
                # Get booked slots for the date
                bookings = Booking.objects.filter(
                    reservation_date=date,
                    first_name__isnull=False,
                    first_name__gt=''
                ).order_by('reservation_slot')
                
                booked_slots = list(bookings.values_list('reservation_slot', flat=True))
                
                # Get available slots
                available_slots = [slot for slot in ALL_TIME_SLOTS if slot not in booked_slots]
                
                # Format bookings for display
                bookings_data = [{
                    'first_name': booking.first_name,
                    'reservation_slot': booking.reservation_slot
                } for booking in bookings]
                
                return JsonResponse({
                    'available_slots': available_slots,
                    'bookings': bookings_data,
                    'total_slots': len(ALL_TIME_SLOTS),
                    'available_count': len(available_slots),
                    'booked_count': len(booked_slots)
                })
                
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            except Exception as e:
                return JsonResponse({
                    'error': 'Failed to fetch bookings',
                    'details': str(e)
                }, status=500)
        else:
            # This is a template request - show all upcoming bookings
            today = datetime.now().date()
            bookings = Booking.objects.filter(
                reservation_date__gte=today,
                first_name__isnull=False,
                first_name__gt=''
            ).order_by('reservation_date', 'reservation_slot')
            
            context = {
                'bookings': bookings,
                'current_date': today.strftime('%B %d, %Y')
            }
            
            return render(request, 'bookings.html', context)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

def reservations(request):
    today = datetime.now().date()
    
    # Get all upcoming bookings
    bookings = Booking.objects.filter(
        reservation_date__gte=today,
        first_name__isnull=False,
        first_name__gt=''
    ).order_by('reservation_date', 'reservation_slot')
    
    context = {
        'bookings': bookings,
        'current_date': today.strftime('%B %d, %Y')
    }
    
    return render(request, 'bookings.html', context)
