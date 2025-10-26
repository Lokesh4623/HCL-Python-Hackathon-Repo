# HCL-Python-Hackathon-Repo
HCL - Python Hackathon Task Repository

**API Flow:**

1. User → Request JWT (/generate-token) → FastAPI validates PAN → Returns JWT → 
2. User → Create Account (/pan/{pan_number}/create-account) with JWT → 
    FastAPI verifies JWT & PAN → Validates deposit → Creates Account → Returns Success Message → 
3. User → Fetch Accounts (/pan/{pan_number}/accounts) with JWT → FastAPI returns Account List

