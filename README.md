# IPT2
IPT Final Drill 1.0
# Online Selling Platform API
-This Flask API provides a backend for an online selling platform, featuring user authentication, product management, and user management.

## Features
- **User Authentication**: Secure login with JWT tokens.
- **Product Management**: CRUD operations for products.
- **User Management**: CRUD operations for users.
- **Flexible Data Format**: Supports both JSON and XML data formats.

## Configuration
Before running the application, ensure the following configurations are set in `app.config`:
- `MYSQL_HOST`: Database host (default is "localhost").
- `MYSQL_USER`: Database user (default is "root").
- `MYSQL_PASSWORD`: Database password (default is "admin").
- `MYSQL_DB`: Database name (default is "online_selling").
- `MYSQL_CURSORCLASS`: Cursor class (default is "DictCursor").
- `JWT_SECRET_KEY`: Secret key for JWT token generation (change this to a random secret key).

## Installation
To set up the project environment, follow these steps:
1. Clone the repository to your local machine.
2. Create a virtual environment:

## python -m venv venv
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```
4. Install the required packages:

## Running the Application
To run the application, use the following command:
**FLASK**

The API will be available at `http://localhost:5000`.

## Endpoints

### User Authentication
- **POST /login**: Authenticate a user and return a JWT token.

### Product Routes
- **GET /products**: Retrieve a list of products.
- **POST /products**: Add a new product.
- **PUT /products/<product_id>**: Update an existing product.
- **DELETE /products/<product_id>**: Delete a product.

### User Routes
- **GET /users**: Retrieve a list of users.
- **POST /users**: Add a new user.
- **PUT /users/<user_id>**: Update an existing user.
- **DELETE /users/<user_id>**: Delete a user.

### Protected Route
- **GET /protected**: A protected route that requires a valid JWT token.
## Testing
Ensure to write unit tests for your API endpoints. Use the `unittest` framework to create test cases and validate the functionality of your application.
