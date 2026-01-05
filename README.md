# DjangoRedditProject

A production-oriented **Reddit-like** social media platform built with **Django**, **Django REST Framework**, **FastAPI**, **PostgreSQL**, **Redis**, and **Nginx**.

This project demonstrates:
- scalable backend architecture
- real-time features with **WebSockets**
- complex relational data modeling
- comparison between **DRF** and **FastAPI** approaches

---

## ✅ Key Features

### 🧑‍🤝‍🧑 Authentication & Authorization
- User registration, login, logout
- JWT authentication via **DRF SimpleJWT**
- Permission-based access control

### 📝 Posts & Comments
- Posts with rich relationships (FK, M2M)
- Nested comments (up to **6 levels**, Reddit-style)
- Optimized comment tree rendering

### ❤️ Social Interactions
- Likes for posts and comments
- Subscriptions / following system
- Personalized interactions

### 🔔 Notifications
Real-time notifications triggered by:
- likes
- comments
- new subscriptions  
Delivered via **WebSockets**

### 💬 Real-time Chat
- Private user-to-user chats
- Built with **Django Channels + WebSockets**
- Auto-scroll to latest message (JS)
- Redis-backed channel layer (**channels-redis**)

---

## ⚡ Performance & Scalability
- PostgreSQL with indexing & query optimization
- Redis used as a **low-level cache** (raw Redis, not django-redis)
- Reduced DB load via caching and async handling
- Separation of concerns + production-oriented settings

---

## 📦 API Layer

### Django REST Framework
- REST API with JWT auth
- Swagger / OpenAPI docs

### FastAPI (experimental)
- Separate implementation for benchmarking
- Demonstrates async-first API design

---

## 🛠 Admin Panel
- Customized admin UI with **django-jazzmin**

---

## 🎨 Frontend
- Django templates (SSR)
- **HTMX** for dynamic UI updates
- Vanilla JavaScript
- Custom Django template tags

---

## 📡 Deployment & Infrastructure
- Deployed on a remote Linux server
- **Nginx** as reverse proxy
- **Uvicorn / Daphne** as ASGI servers
- Docker-ready architecture
- Prepared for background jobs (Celery-ready)

---

## 🧰 Tech Stack

**Backend:** Django 5.2, DRF, FastAPI, Django Channels  
**Database:** PostgreSQL (SQLAlchemy – experimental)  
**Cache/Messaging:** Redis, channels-redis  
**Auth:** JWT (SimpleJWT), Django auth  
**Realtime:** WebSockets  
**Frontend:** Django templates, HTMX, JavaScript  
**Infra:** Nginx, Uvicorn, Daphne, Docker-ready  
**Other:** drf-yasg, drf-spectacular, django-cors-headers, Pillow

---

## 🗂️ Project Structure (high-level)
> Adjust names if yours differ.

- `config/` – Django settings, urls, ASGI/WSGI
- `apps/` – main Django apps (posts, comments, chat, notifications, users)
- `templates/` – Django templates
- `static/` – frontend assets (JS/CSS)
- `fastapi_app/` – experimental FastAPI implementation
- `nginx/` – nginx configs (if included)
- `docker/` – docker configs (if included)

---

## ⚙️ Local Installation

### 1) Clone repository
```bash
git clone https://github.com/Oleg21345/DjangoReditProject.git
cd DjangoReditProject


python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
