# HCL-Python-Hackathon-Repo
HCL - Python Hackathon Task Repository

**Flow Diagram:**

User (Client)
    │
    │ 1. Request JWT with PAN
    ▼
FastAPI Server (/generate-token)
    │
    │ 2. Validate PAN
    │    └─ If valid → Generate JWT
    │    └─ If invalid → Return error
    ▼
JWT Token sent to User
    │
    │ 3. Send account creation request with JWT
    ▼
FastAPI Server (/pan/{pan_number}/create-account)
    │
    │ 4. Verify JWT
    │    └─ If valid → Validate PAN & Deposit → Create Account
    │    └─ If invalid → Return error
    ▼
Success Message:
"Your Savings/FD/Current account created successfully with account number XXX"
    │
    │ 5. Optional: Fetch accounts with JWT
    ▼
FastAPI Server (/pan/{pan_number}/accounts)
    │
    ▼
List of User Accounts returned
