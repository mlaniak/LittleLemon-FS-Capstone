# Little Lemon Restaurant API

This project implements REST APIs for the Little Lemon restaurant using Django and Django REST Framework.

## Features

- Menu API: Allows customers to browse and order food items
- Table Booking API: Enables customers to reserve tables for specific dates and party sizes
- User Authentication: Secure token-based authentication using Djoser and Django REST Framework
  - User registration with email
  - Token-based authentication
  - User profile management

## Technical Stack

- Python 3.x
- Django 5.1.6
- Django REST Framework 3.14.0
- Djoser 2.3.1
- Django REST Framework SimpleJWT 5.4.0
- MySQL Database

## API Endpoints

### Authentication
- POST `/api/api-token-auth/`
  - Get authentication token
  - Required fields: username, password
  - Returns: token

### Menu Operations
- GET `/api/menu/`
  - List all menu items
  - No authentication required
- GET `/api/menu/{id}/`
  - Get specific menu item
  - No authentication required
- POST `/api/menu/`
  - Create new menu item
  - Requires authentication
  - Fields: title, price, inventory

### Table Booking Operations
- GET `/api/bookings/`
  - List all bookings
  - Requires authentication
- POST `/api/bookings/`
  - Create new booking
  - Requires authentication
  - Fields: name, no_of_guests, bookingdate
- GET `/api/bookings/{id}/`
  - Get specific booking
  - Requires authentication
- PUT `/api/bookings/{id}/`
  - Update booking
  - Requires authentication
  - Fields: name, no_of_guests, bookingdate
- DELETE `/api/bookings/{id}/`
  - Delete booking
  - Requires authentication

### Menu API
- GET /api/menu/ - List all menu items
- POST /api/menu/ - Add new menu item
- GET /api/menu/{id}/ - Get specific menu item
- PUT /api/menu/{id}/ - Update menu item
- DELETE /api/menu/{id}/ - Delete menu item

### Booking API
- GET /api/booking/ - List all bookings
- POST /api/booking/ - Create new booking
- GET /api/booking/{id}/ - Get specific booking
- PUT /api/booking/{id}/ - Update booking
- DELETE /api/booking/{id}/ - Delete booking

### API Response Format

All API endpoints return responses in a consistent format:

Success Response:
```json
{
    "status": "success",
    "data": { ... }
}
```

Error Response:
```json
{
    "status": "error",
    "errors": { ... }
}
```

## Project Setup

### Prerequisites

1. Python 3.x installed on your system
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during Windows installation

2. MySQL installed on your system
   - [MySQL Community Downloads](https://dev.mysql.com/downloads/)
   - For Windows: MySQL Installer
   - For macOS: Use Homebrew: `brew install mysql`

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd LittleLemon-FS-Capstone
```

2. Create and activate virtual environment:

For Windows:
```bash
python -m venv myenv
myenv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies:
```bash
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### Database Setup

For Windows:
```bash
# If using MySQL, make sure MySQL is running in Services
# Create database
mysql -u root -p
CREATE DATABASE littlelemon;
```

For macOS:
```bash
# Start MySQL if not running
brew services start mysql
# Create database
mysql -u root -p
CREATE DATABASE littlelemon;
```

3. Apply database migrations:
```bash
cd littlelemon
python manage.py migrate
```

4. Run development server:
```bash
python manage.py runserver
```

The server will start at http://localhost:8000/

## Authentication Instructions
1. Obtain token by sending POST request to `/api/api-token-auth/` with username and password
2. Include token in request header for authenticated endpoints:
   ```
   Authorization: Token <your-token-here>
   ```

## Testing with Insomnia
1. Import the API collection
2. Get authentication token using the `/api/api-token-auth/` endpoint
3. Set token in request headers for authenticated endpoints
4. Test all endpoints following the API documentation above

## Running Tests
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

## Database Models

### Menu
- id: AutoField (primary key)
- title: CharField(max_length=255)
- price: DecimalField(max_digits=10, decimal_places=2)
- inventory: IntegerField

### Booking
- id: AutoField (primary key)
- name: CharField(max_length=255)
- no_of_guests: IntegerField
- bookingdate: DateTimeField

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
