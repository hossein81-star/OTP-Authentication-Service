# 🔐 OTP Authentication Service

A production-inspired authentication service built with **Django**, **Django REST Framework**, **PostgreSQL**, **Redis**, **Celery**, **JWT**, and **Docker**.

This project implements a complete passwordless authentication system using **Phone Number + One-Time Password (OTP)**. It includes rate limiting, cooldown protection, asynchronous task processing, JWT authentication, refresh token blacklisting, and a fully containerized development environment.

---

# ✨ Features

### Authentication

* ✅ Custom User Model
* ✅ Phone Number Authentication
* ✅ User Registration with OTP
* ✅ User Login with OTP
* ✅ JWT Authentication
* ✅ Access Token
* ✅ Refresh Token
* ✅ Secure Logout (Refresh Token Blacklisting)

---

### OTP System

* ✅ Random OTP Generation
* ✅ OTP Expiration
* ✅ OTP Verification
* ✅ Redis-based OTP Storage
* ✅ Automatic OTP Cleanup

---

### Security

* ✅ Rate Limiting
* ✅ Cooldown Mechanism
* ✅ Failed OTP Attempt Tracking
* ✅ Temporary User Blocking
* ✅ Redis Cache Isolation
* ✅ JWT Blacklist Support

---

### Background Tasks

* ✅ Celery Worker
* ✅ Asynchronous OTP Sending

---

### Infrastructure

* ✅ Docker
* ✅ Docker Compose
* ✅ PostgreSQL
* ✅ Redis
* ✅ RedisInsight
* ✅ OpenAPI / Swagger Documentation

---

# 🛠 Tech Stack

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python 3.12           | Programming Language        |
| Django                | Backend Framework           |
| Django REST Framework | REST APIs                   |
| PostgreSQL            | Relational Database         |
| Redis                 | OTP Cache & Rate Limiting   |
| Celery                | Background Tasks            |
| JWT                   | Authentication              |
| Docker                | Containerization            |
| Docker Compose        | Multi-container Environment |
| drf-spectacular       | API Documentation           |

---

# 🏗 Architecture

```text
                   Client
                      │
                      ▼
             Django REST API
                      │
        ┌─────────────┼──────────────┐
        │             │              │
        ▼             ▼              ▼
 PostgreSQL        Redis         JWT Service
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
    OTP Cache     Cooldown      Failed Attempts
                      │
                      ▼
               Celery Worker
                      │
                      ▼
                 SMS Provider
```

---

# 🔄 Authentication Flow

## Registration

```text
Phone Number
      │
      ▼
Send OTP API
      │
      ▼
Generate OTP
      │
      ▼
Store OTP in Redis
      │
      ▼
Celery Worker
      │
      ▼
Send SMS
      │
      ▼
Verify OTP
      │
      ▼
Create User
      │
      ▼
Generate JWT Tokens
```

---

## Login

```text
Phone Number
      │
      ▼
Send OTP
      │
      ▼
Redis
      │
      ▼
Verify OTP
      │
      ▼
Generate Access Token
      │
      ▼
Generate Refresh Token
```

---

## Logout

```text
Authenticated User
        │
        ▼
Send Refresh Token
        │
        ▼
Blacklist Refresh Token
        │
        ▼
Logout Successfully
```

---

# 🔒 Security Mechanisms

The authentication system includes several security layers:

* OTP expiration using Redis TTL
* Cooldown between OTP requests
* Rate limiting per phone number
* Failed OTP attempt tracking
* Temporary user blocking
* Refresh Token Blacklisting
* Passwordless authentication
* Temporary cache cleanup after successful authentication

---

# 📦 Docker Services

The application runs using multiple Docker containers.

| Service      | Description         |
| ------------ | ------------------- |
| backend      | Django REST API     |
| postgres     | PostgreSQL Database |
| redis        | Redis Cache         |
| celery       | Celery Worker       |
| redisinsight | Redis GUI           |

Run the project with:

```bash
docker compose up --build
```

---



# 📖 API Documentation

Swagger UI:

```text
http://localhost:8000/api/schema/swagger-ui/
```

OpenAPI Schema:

```text
http://localhost:8000/api/schema/
```

---

# 🚀 Future Improvements

* Email Verification
* Unit Tests
* Integration Tests
* GitHub Actions CI/CD
* Nginx
* Production Docker Configuration
* Monitoring & Logging


---

# 🎯 Learning Objectives

This project was created to gain practical experience with:

* Django REST Framework
* Authentication System Design
* Redis
* Celery
* Docker
* JWT Authentication
* PostgreSQL
* RESTful API Development
* Background Task Processing
* Scalable Backend Architecture

---

# 👨‍💻 Author

**Hossein81**

Backend Developer

Python • Django • Django REST Framework
