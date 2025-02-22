# Little Lemon API Testing Guide

This guide explains how to test the Little Lemon Restaurant API using Insomnia REST Client.

## Setup Instructions

1. Download and install [Insomnia](https://insomnia.rest/download)
2. Open Insomnia
3. Click on `Create` > `Import from File`
4. Select the `insomnia_collection.json` file from this repository
5. The collection "Little Lemon API" will be imported with all requests

## Collection Structure

The collection is organized into three main folders:

1. **Authentication**
   - Register User
   - Login
   - Logout

2. **Menu**
   - List Categories
   - Create Category
   - List Menu Items
   - Create Menu Item

3. **Bookings**
   - List Bookings
   - Create Booking

## Testing Flow

1. **Start the Django Server**
   ```bash
   python manage.py runserver
   ```

2. **User Registration and Authentication**
   - Use the "Register User" request to create a new account
   - Use the "Login" request to get an authentication token
   - The token will be automatically used in subsequent requests

3. **Menu Management**
   - Create a category using "Create Category"
   - Create menu items and assign them to categories
   - View all menu items and categories

4. **Booking Management**
   - Create table bookings
   - View all bookings (requires authentication)

## API Endpoints

### Authentication
- `POST /auth/users/` - Register new user
- `POST /auth/token/login/` - Get authentication token
- `POST /auth/token/logout/` - Invalidate token

### Menu
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/menu/` - List all menu items
- `POST /api/menu/` - Create new menu item

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking

## Response Formats

### Success Responses
- **200 OK** - Request successful
- **201 Created** - Resource created successfully

### Error Responses
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found

## Testing Tips

1. Always test the authentication flow first
2. Create categories before creating menu items
3. Check for duplicate bookings in the same time slot
4. Verify that unauthenticated users can only read menu items
5. Ensure all required fields are provided in POST requests
