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



