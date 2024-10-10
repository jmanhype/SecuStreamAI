# SecuStreamAI API Documentation

## Overview

This document provides details on the API endpoints available in SecuStreamAI.

## API Versioning

This API uses versioning in the URL path. The current version is v1. All endpoints should be prefixed with `/api/v1/`.

## Common Headers

Request headers:
- `Content-Type: application/json`
- `Authorization: Bearer <your_jwt_token>`

Response headers:
- `Content-Type: application/json`

## Authentication

All API requests require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Authentication Endpoint

- **URL:** `/api/v1/auth/token`
- **Method:** POST
- **Description:** Obtain a JWT token for authentication
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **Example:**
  ```bash
  curl -X POST "http://localhost:8080/api/v1/auth/token" \
       -H "Content-Type: application/json" \
       -d '{"username": "your_username", "password": "your_password"}'
  ```

## Rate Limiting

API requests are subject to rate limiting to ensure fair usage. The current limit is 100 requests per minute per IP address. If you exceed this limit, you'll receive a 429 Too Many Requests response.

## Endpoints

### 1. Analyze Security Event

- **URL:** `/api/v1/events/analyze`
- **Method:** POST
- **Description:** Submit a security event for analysis
- **Request Body:**
  ```json
  {
    "context": "string (e.g., 'login', 'file_access', 'network_traffic')",
    "event_description": "string (detailed description of the security event)"
  }
  ```
- **Response:**
  ```json
  {
    "event_id": "string",
    "risk_level": "string",
    "action": "string",
    "analysis": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X POST "http://localhost:8080/api/v1/events/analyze" \
       -H "Authorization: Bearer <your_jwt_token>" \
       -H "Content-Type: application/json" \
       -d '{"context": "login", "event_description": "Failed login attempt from IP 192.168.1.100"}'
  ```

### 2. Retrieve Analysis Results

- **URL:** `/api/v1/events/{event_id}`
- **Method:** GET
- **Description:** Retrieve analysis results for a specific event
- **Parameters:**
  - `event_id`: string (path parameter)
- **Response:**
  ```json
  {
    "event_id": "string",
    "context": "string",
    "event_description": "string",
    "risk_level": "string",
    "action": "string",
    "analysis": "string",
    "analysis_method": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:8080/api/v1/events/12345" \
       -H "Authorization: Bearer <your_jwt_token>"
  ```

### 3. List Recent Events

- **URL:** `/api/v1/events`
- **Method:** GET
- **Description:** Retrieve a list of recent security events
- **Query Parameters:**
  - `limit`: integer (optional, default: 50)
  - `offset`: integer (optional, default: 0)
- **Response:**
  ```json
  {
    "total": integer,
    "events": [
      {
        "event_id": "string",
        "context": "string",
        "event_description": "string",
        "risk_level": "string",
        "timestamp": "string"
      }
    ]
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:8080/api/v1/events?limit=10&offset=0" \
       -H "Authorization: Bearer <your_jwt_token>"
  ```

### 4. Get Analysis Methods Statistics

- **URL:** `/api/v1/events/analysis_methods`
- **Method:** GET
- **Description:** Retrieve statistics on analysis methods used
- **Response:**
  ```json
  {
    "total_events": integer,
    "rule_based": integer,
    "pytorch_model": integer,
    "dspy_llm": integer
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:8080/api/v1/events/analysis_methods" \
       -H "Authorization: Bearer <your_jwt_token>"
  ```

### 5. Trigger Model Fine-tuning

- **URL:** `/api/v1/models/finetune`
- **Method:** POST
- **Description:** Manually trigger the model fine-tuning process
- **Response:**
  ```json
  {
    "status": "string",
    "message": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X POST "http://localhost:8080/api/v1/models/finetune" \
       -H "Authorization: Bearer <your_jwt_token>"
  ```

### 6. Create User

- **URL:** `/api/v1/users`
- **Method:** POST
- **Description:** Create a new user account
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string"
  }
  ```
- **Response:**
  ```json
  {
    "user_id": "string",
    "username": "string",
    "email": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X POST "http://localhost:8080/api/v1/users" \
       -H "Content-Type: application/json" \
       -d '{"username": "new_user", "password": "secure_password", "email": "user@example.com"}'
  ```

### 7. Get User Profile

- **URL:** `/api/v1/users/me`
- **Method:** GET
- **Description:** Retrieve the profile of the authenticated user
- **Response:**
  ```json
  {
    "user_id": "string",
    "username": "string",
    "email": "string",
    "created_at": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:8080/api/v1/users/me" \
       -H "Authorization: Bearer <your_jwt_token>"
  ```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request:** Invalid input data
- **401 Unauthorized:** Missing or invalid authentication token
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Requested resource not found
- **429 Too Many Requests:** Rate limit exceeded
- **500 Internal Server Error:** Server-side error

Error response body:
```json
{
  "error": "string",
  "detail": "string"
}
```