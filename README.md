# HCL-Python-Hackathon-Repo
HCL - Python Hackathon Task Repository

**1. Architecture**

The application follows a layered design:

Client (Postman/Browser) ---> FastAPI API Layer ---> Business Logic & Security  ---> PostgreSQL Database

Client: Sends HTTP requests (register, login, create account).

API Layer: Handles routing, validation, and authentication.

Business Logic & Security: Validates inputs, hashes passwords, generates unique account numbers, enforces rules.

Database: Stores users and accounts persistently.

----------------------------------------------------------------------------------------------------------------------------------

**2. Database Design**

**Users Table**

Column	Type	Description
id	int	Primary key
username	str	Unique login
hashed_password	str	Bcrypt-hashed password

**Accounts Table**

Column	Type	Description
id	int	Primary key
account_number	str	Unique account number with type prefix
customer_name	str	Account holder name
account_type	str	Savings / Current / FD
balance	float	Initial deposit
user_id	int	Foreign key linking account to user

----------------------------------------------------------------------------------------------------------------------------------

**3. Security**

Password Hashing: bcrypt via Passlib ensures passwords are stored securely.

JWT Authentication: Users receive a token after login/registration to access protected endpoints.

Protected Routes: Account creation and listing require a valid JWT.

----------------------------------------------------------------------------------------------------------------------------------

**4. Account Creation Logic**

Validate input fields (name, type, deposit).

Enforce minimum deposit per account type:

Savings: ₹1000

Current: ₹5000

FD: ₹10000

Generate a unique 12-character account number with type prefix:

SAV → Savings, CUR → Current, FD → Fixed Deposit

Save account in PostgreSQL linked to the authenticated user.

----------------------------------------------------------------------------------------------------------------------------------

**5. API Endpoints**

Endpoint	       Method	  Description

/register	       POST	    Register new user, returns JWT

/token	         POST	    User login, returns JWT

/create-account	 POST	    Create a new account (JWT required)

/accounts	       GET	    List all accounts of the authenticated user

----------------------------------------------------------------------------------------------------------------------------------

