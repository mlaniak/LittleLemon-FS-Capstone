# Little Lemon Restaurant API

This project implements REST APIs for the Little Lemon restaurant using Django and Django REST Framework.

## Features

- Menu Management: Browse, create, and manage menu items and categories
- Table Booking System: Reserve tables for specific dates and time slots
- User Authentication: Secure token-based authentication using Djoser
- Admin Interface: Django admin panel for easy content management

## Technical Stack

- Python 3.x
- Django 5.1.6
- Django REST Framework 3.14.0
- Djoser 2.3.1
- MySQL Database

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure MySQL database in settings.py
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- POST `/auth/users/` - User registration
- POST `/auth/token/login/` - Get authentication token
- POST `/auth/token/logout/` - Logout (invalidate token)

### Menu Management
- GET, POST `/api/menu/` - List or create menu items
- GET, PUT, DELETE `/api/menu/{id}/` - Retrieve, update or delete menu item
- GET, POST `/api/categories/` - List or create categories
- GET, PUT, DELETE `/api/categories/{id}/` - Retrieve, update or delete category

### Booking System
- GET, POST `/api/bookings/` - List or create bookings
- GET, PUT, DELETE `/api/bookings/{id}/` - Retrieve, update or delete booking

## Authentication

Most endpoints require authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token>
```

## Models

### Menu
- title (string)
- price (decimal)
- inventory (integer)
- description (text)
- category (foreign key)

### Category
- name (string)
- order (integer)

### Booking
- first_name (string)
- reservation_date (date)
- reservation_slot (string)

## Testing

The project includes comprehensive unit tests for all models and API endpoints. Run tests with:
```bash
python manage.py test
```

## Project Structure

```
littlelemon/
├── manage.py
├── littlelemon/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── restaurant/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    └── views.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
