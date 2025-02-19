# Little Lemon Restaurant API

This project implements REST APIs for the Little Lemon restaurant using Django and Django REST Framework.

## Features

- Menu API: Allows customers to browse and order food items
- Table Booking API: Enables customers to reserve tables for specific dates and party sizes

## Technical Stack

- Python 3.x
- Django 5.1.6
- Django REST Framework 3.14.0
- MySQL Database

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

## API Endpoints

### Menu API
- GET /api/menu/ - List all menu items
- POST /api/menu/ - Add new menu item
- GET /api/menu/{id}/ - Get specific menu item
- PUT /api/menu/{id}/ - Update menu item
- DELETE /api/menu/{id}/ - Delete menu item

### Table Booking API
- GET /api/bookings/ - List all bookings
- POST /api/bookings/ - Create new booking
- GET /api/bookings/{id}/ - Get specific booking
- PUT /api/bookings/{id}/ - Update booking
- DELETE /api/bookings/{id}/ - Delete booking

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

### Menu Item
- name: CharField
- price: DecimalField
- description: TextField
- category: CharField

### Table Booking
- date: DateField
- time: TimeField
- party_size: IntegerField
- name: CharField
- email: EmailField
- phone: CharField

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
