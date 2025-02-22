# Little Lemon Restaurant API Documentation

## API Endpoints

### Authentication
- POST /api/api-token-auth/
  - Get authentication token
  - Required fields: username, password
  - Returns: token

### Menu Operations
- GET /api/menu/
  - List all menu items
  - No authentication required
- GET /api/menu/{id}/
  - Get specific menu item
  - No authentication required
- POST /api/menu/
  - Create new menu item
  - Requires authentication
  - Fields: title, price, inventory

### Table Booking Operations
- GET /api/bookings/
  - List all bookings
  - Requires authentication
- POST /api/bookings/
  - Create new booking
  - Requires authentication
  - Fields: name, no_of_guests, bookingdate
- GET /api/bookings/{id}/
  - Get specific booking
  - Requires authentication
- PUT /api/bookings/{id}/
  - Update booking
  - Requires authentication
  - Fields: name, no_of_guests, bookingdate
- DELETE /api/bookings/{id}/
  - Delete booking
  - Requires authentication

## Authentication Instructions
1. Obtain token by sending POST request to /api/api-token-auth/ with username and password
2. Include token in request header for authenticated endpoints:
   Authorization: Token <your-token-here>

## Testing with Insomnia
1. Import the API collection
2. Get authentication token
3. Set token in request headers
4. Test endpoints
