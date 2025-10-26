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

-----------------------------------------------------------------------------------------

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

Errors:

400 Bad Request → Invalid PAN format

404 Not Found → User not found

-----------------------------------------------------------------------------------------

**2. Create Account**

POST /accounts/create

Description:
Creates a new account (Savings, Current, or FD) for a user. Requires JWT authentication.

Headers

Authorization: Bearer <jwt_token>

Request Body (JSON)

{
  "pan_number": "ABCDE1234F",
  "account_type": "Savings",
  "initial_deposit": 2000
}


Responses

200 OK

{
  "message": "Your Savings account created successfully with the account number SAV000000001"
}

**Validation Rules:**

PAN must match the format: 5 letters + 4 digits + 1 letter (^[A-Z]{5}[0-9]{4}[A-Z]{1}$)

Account type must be one of: "Savings", "Current", "FD"

Minimum deposits:

Savings: 1000

Current: 5000

FD: 10000

**Errors:**

400 Bad Request → Invalid PAN or invalid account type or insufficient initial deposit

401 Unauthorized → Missing/invalid JWT token

403 Forbidden → JWT does not match PAN

404 Not Found → User not found

-----------------------------------------------------------------------------------------

**3. Get Accounts**

POST /accounts

Headers

Authorization: Bearer <jwt_token>

Request Body:

{
  "pan_number": "ABCDE1234F"
}


Response:

200 OK

[
  {
    "account_number": "SAV000000001",
    "account_type": "Savings",
    "balance": 2000
  },
  {
    "account_number": "CUR000000002",
    "account_type": "Current",
    "balance": 5000
  }
]

**Validation Rules:**

PAN must match the format: 5 letters + 4 digits + 1 letter

**Errors:**

400 Bad Request → Invalid PAN format

401 Unauthorized → Missing/invalid JWT token

403 Forbidden → JWT does not match PAN

404 Not Found → User not found

-----------------------------------------------------------------------------------------

**Authentication**

All account-related endpoints require a JWT token generated via /generate-token.

JWT should be sent in the Authorization header as a Bearer token:

_Authorization: Bearer <jwt_token>_

**JWT Generation**

1.Server receives user data (e.g., PAN).

2.Validate user exists in database.

3.Create a payload with data, datetime and expiry.

4.Generate JWT using:
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

5.Return the JWT to the client.

**JWT Validation**

1.Client sends JWT in Authorization: Bearer <token> header.

2.Server extracts token (token = authorization[7:]).

3.Decode and verify token using:
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

4.Check for validity:

  Signature matches SECRET_KEY, Algorithm matches "HS256", Token not expired

5.Use payload data (e.g., PAN) for authorization.

6.If invalid or expired → return 401 Unauthorized.

-----------------------------------------------------------------------------------------

**Database Design:**

**1. Users Table (Existing)**

| Column     | Type         | Constraints                 | Description      |
| ---------- | ------------ | --------------------------- | ---------------- |
| id         | INTEGER      | PRIMARY KEY, AUTO INCREMENT | Internal user ID |
| pan_number | VARCHAR(10)  | UNIQUE, NOT NULL            | PAN number       |
| name       | VARCHAR(100) | NULLABLE                    | User full name   |

**Assumption: This table is already preloaded.**

**2.Accounts Table (New)**

| Column         | Type        | Constraints                 | Description                                        |
| -------------- | ----------- | --------------------------- | -------------------------------------------------- |
| id             | INTEGER     | PRIMARY KEY, AUTO INCREMENT | Internal account ID                                |
| account_number | VARCHAR(12) | UNIQUE, NOT NULL            | Account number (prefix + 12-digit padded sequence) |
| account_type   | VARCHAR(20) | NOT NULL                    | Type: Savings / Current / FD                       |
| balance        | FLOAT       | NOT NULL                    | Current account balance                            |
| user_id        | INTEGER     | FOREIGN KEY → users(id)     | Owner of the account                               |
| created_at     | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP   | Account creation timestamp                         |


**3. Relationships**

User → Account = 1-to-many

Account → User = many-to-1

