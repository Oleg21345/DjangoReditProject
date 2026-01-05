# DjangoRedditProject

A production-oriented Reddit-like social media platform built with **Django**, **Django REST Framework**, **FastAPI**, **PostgreSQL**, **Redis**, and **Nginx**.

The project demonstrates scalable backend architecture, real-time features with WebSockets, complex relational data modeling, and a comparison between classic Django REST APIs and FastAPI-based services.

---

## 🚀 Key Features

### 🧑‍🤝‍🧑 Authentication & Authorization
- User registration, login, logout
- JWT-based authentication using **DRF SimpleJWT**
- Permission-based access control

### 📝 Posts & Comments
- Reddit-style posts with rich relationships
- **Multi-level nested comments (up to 6 levels deep)**
- Optimized comment tree rendering

### ❤️ Social Interactions
- Likes for posts and comments
- User subscriptions and following system
- Personalized content interactions

### 🔔 Notifications System
- Real-time notifications triggered by:
  - Likes
  - Comments
  - New subscriptions
- Delivered via WebSockets

### 💬 Real-time Chat
- Private user-to-user chats
- Built with **Django Channels + WebSockets**
- Auto-scroll to the latest messages (JavaScript)
- Redis-backed channel layer

---

## ⚡ Performance & Scalability
- PostgreSQL with optimized queries and indexing
- Redis used as a **low-level cache** (without django-redis)
- Reduced DB load via caching and async handling
- Production-ready settings and separation of concerns

---

## 📦 API Layer
- **Django REST Framework**
  - RESTful API with JWT auth
  - Swagger / OpenAPI documentation
- **FastAPI (experimental)**
  - Separate implementation for benchmarking and performance comparison
  - Demonstrates async-first API design

---

## 🛠 Admin Panel
- Customized Django admin using **django-jazzmin**
- Improved usability for moderators and admins

---

## 🎨 Frontend
- Server-rendered Django templates
- **HTMX** for dynamic UI updates
- Vanilla JavaScript for client-side interactions
- Custom Django template tags

---

## 📡 Deployment & Infrastructure
- Deployed on a remote Linux server
- **Nginx** as reverse proxy
- **Uvicorn / Daphne** as ASGI servers
- Docker-ready architecture
- Prepared for background jobs (Celery-ready)

---

## 🛠 Tech Stack

**Backend**
- Django 5.2
- Django REST Framework
- FastAPI
- Django Channels

**Database**
- PostgreSQL
- SQLAlchemy (experimental)

**Cache / Messaging**
- Redis
- channels-redis

**Authentication**
- JWT (SimpleJWT)
- Django auth system

**Realtime**
- WebSockets

**Frontend**
- Django templates
- HTMX
- JavaScript

**Infrastructure**
- Nginx
- Uvicorn
- Daphne
- Docker (ready)

**Other**
- drf-yasg
- drf-spectacular
- django-cors-headers
- Pillow

---

## ⚙️ Local Installation

### 1️⃣ Clone repository
```bash
git clone https://github.com/Oleg21345/DjangoReditProject.git
cd DjangoReditProject


python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
