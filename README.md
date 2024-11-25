![Flask Logo](https://flask.palletsprojects.com/en/stable/_images/flask-horizontal.png)
![Docker Logo](https://blog.codewithdan.com/wp-content/uploads/2023/06/Docker-Logo.png)

## Docker Setup
To run the project using Docker, follow these steps:

1. **Build Docker Image**
   ```commandline
   docker build -t authorization-api .
   ```

2. **Run Docker Container**
   ```commandline
   docker run -p 5001:5001 authorization-api
   ```

## API Requests
All API requests can be accessed at:
```commandline
http://127.0.0.1:5001
```

### Endpoints

#### 1. `/register` - Register a new user
- **Method**: POST
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  - `201 Created` - User registered successfully
  - `400 Bad Request` - Username already exists or missing fields

#### 2. `/login` - User login to receive an access token
- **Method**: POST
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  - `200 OK` - Returns a JWT token for authorization
  - `401 Unauthorized` - Invalid username or password

#### 3. `/save` - Save a new task for the logged-in user
- **Method**: POST
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "task_name": "My Task 1",
    "status": "Pending",
    "config": {
      "test": "Українська"
    },
    "selectors": ["selector1", "selector2"]
  }
  ```
- **Response**:
  - `201 Created` - Task saved successfully
  - `400 Bad Request` - Missing required fields
  - `500 Internal Server Error` - Error saving the task

#### 4. `/tasks` - Get all saved tasks for the logged-in user
- **Method**: GET
- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`
- **Response**:
  - `200 OK` - Returns a list of saved tasks
  - `404 Not Found` - User not found

