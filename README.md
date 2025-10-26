# HCL-Python-Hackathon-Repo
HCL - Python Hackathon Task Repository

**PAN-Based Account Creation API with JWT**

This API allows users to generate JWT tokens based on their PAN, create different types of bank accounts (Savings, Current, FD), and retrieve account details. All account-related endpoints require JWT-based authorization.

**PAN Format Validation**

PAN must match the regex: ^[A-Z]{5}[0-9]{4}[A-Z]{1}$

Example of valid PAN: ABCDE1234F

**Account Types**

| Type    | Minimum Deposit |
| ------- | --------------- |
| Savings | 1000            |
| Current | 5000            |
| FD      | 10000           |


**Endpoints**

**1. Generate JWT Token**

POST /generate-token

Request Body (JSON)

{
  "pan_number": "ABCDE1234F"
}

Responses

200 OK
{
  "jwt": "<generated_token>"
}

400 Bad Request – Invalid PAN format

404 Not Found – PAN not registered

**2. Create Account**

POST /pan/{pan_number}/create-account

Headers

Authorization: Bearer <jwt_token>


Path Parameter

pan_number – PAN of the user (validated via regex)

Request Body (JSON)

{
  "account_type": "Savings",
  "initial_deposit": 2000
}


Responses

200 OK

{
  "message": "Your Savings account created successfully with the account number 1234567890"
}


400 Bad Request – Invalid PAN, invalid account type, or deposit below minimum

401 Unauthorized – Missing or malformed Bearer token

403 Forbidden – Token PAN does not match path PAN

404 Not Found – PAN not registered

**3. Get Accounts for PAN**

GET /pan/{pan_number}/accounts

Headers

Authorization: Bearer <jwt_token>


Path Parameter

pan_number – PAN of the user (validated via regex)

Responses

200 OK

[
  {
    "account_number": "1234567890",
    "account_type": "Savings",
    "balance": 2000
  },
  {
    "account_number": "1234567891",
    "account_type": "FD",
    "balance": 15000
  }
]




400 Bad Request – Invalid PAN format

401 Unauthorized – Missing or malformed Bearer token

403 Forbidden – Token PAN does not match path PAN

404 Not Found – PAN not registered

**Authentication**

All account-related endpoints require a JWT token generated via /generate-token.

JWT should be sent in the Authorization header as a Bearer token:

_Authorization: Bearer <jwt_token>_
