# DjangoRedditProject

A full-featured Reddit-like social media platform built with **Django**, **FastAPI**, **PostgreSQL**, **Redis**, and **Nginx**.  
This project demonstrates production-level architecture with WebSockets, real-time notifications, multi-level comments, and REST/DRF vs FastAPI comparison.  

---

## 🚀 Features
- 🧑‍🤝‍🧑 **Authentication & Authorization**  
  - User registration, login, logout, JWT tokens (DRF SimpleJWT).  

- 💬 **Chat system**  
  - Real-time chats using **Django Channels + WebSockets**.  
  - Auto-scroll to the latest message (JS).  

- 🔔 **Notifications system**  
  - Triggered when someone likes your post, comments, or subscribes to your profile.  

- 📝 **Comments system**  
  - Supports **6 nested levels** of comments (like Reddit).  

- ❤️ **Social features**  
  - Likes, subscriptions, and following.  

- 🗄️ **Database**  
  - PostgreSQL with rich **relationships** (FK, M2M).  

- 📦 **API**  
  - **Django REST Framework (DRF)** API with **Swagger/OpenAPI** docs.  
  - **FastAPI** implementation (experimental, for benchmarking).  

- ⚡ **Performance**  
  - Caching with **Redis** (not django-redis, but raw Redis).  
  - Config optimized for production.  

- 🛠 **Admin panel**  
  - Customized with **django-jazzmin**.  

- 🎨 **Frontend**  
  - JS + HTMX for interactivity.  
  - Django template tags for custom rendering.  

- 📡 **Deployment**  
  - Deployed via GitHub to remote server.  
  - Served with **Nginx** + Uvicorn/Daphne.  

---

## 🛠 Technologies & Libraries
- **Backend**: Django 5.2, Django REST Framework, FastAPI, Django Channels  
- **Database**: PostgreSQL, SQLAlchemy (experimental)  
- **Cache/Queues**: Redis, Channels-Redis  
- **Auth**: JWT (SimpleJWT), Django auth system  
- **Realtime**: WebSockets, Socket.IO  
- **Frontend**: JS, HTMX, Django templates, template tags  
- **Deployment**: Nginx, Uvicorn, Daphne, Docker-ready  
- **Others**: Celery-ready, drf-yasg, drf-spectacular, django-cors-headers, pillow  

---

## ⚙️ Installation

### 1. Clone repository
```bash
git clone https://github.com/Oleg21345/DjangoReditProject.git
cd DjangoReditProject
