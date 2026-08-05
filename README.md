# ICOSNET DSI Platform

## Description

**ICOSNET DSI Platform** is an internal web application developed for the Information Systems Department (DSI) to improve the traceability and management of internal IT processes.

The platform aims to centralize, structure, and historize important DSI activities such as:

* Application sheet management
* User access management
* Meeting traceability
* Hardware tracking
* Technical history management

The project follows a modular architecture to ensure scalability and maintainability.

---

# Technologies

## Backend

* Python
* Django
* Django REST Framework
* SQLite (development)
* PostgreSQL (planned for production)

## Frontend

* React
* Vite
* JavaScript
* Axios

## Development Tools

* Git / GitHub
* Visual Studio Code
* Docker (planned)

---

# Project Structure

```
Icosnet_Traceability_Platform/

├── backend/        # Django REST API
│
├── frontend/       # React application
│
├── docs/           # Documentation
│
└── README.md
```

---

# Backend Architecture

The backend is organized using a modular Django architecture:

```
backend/

├── apps/
│
├── users/
│       # User management and authentication
│
└── application_sheet/
        # Application Sheet business module
```

Each business functionality will be implemented as an independent Django application.

---

# Implemented Features

## Application Sheet Module

The first implemented business module allows DSI teams to manage application information:

* Application details
* Infrastructure information
* Contracts
* User accesses
* Development information
* Storage
* Integrations
* Backup management
* Intervention history

Business validation rules are integrated directly into the backend models.

---

# API

The backend exposes REST APIs using Django REST Framework.

Example:

```
GET    /api/fiches/
POST   /api/fiches/
GET    /api/fiches/{id}/
PUT    /api/fiches/{id}/
DELETE /api/fiches/{id}/
```

---

# Installation

## Backend

Clone the repository:

```bash
git clone <repository_url>
```

Create and activate the virtual environment:

```bash
python -m venv .venv

source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the backend:

```bash
python manage.py runserver
```

Backend URL:

```
http://127.0.0.1:8000
```

---

## Frontend

Go to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```
http://localhost:5173
```

---

# Development Roadmap

Upcoming features:

* Authentication and authorization
* Role management
* JWT security
* Workflow validation system
* Meeting management module
* Generic accounts module
* Hardware tracking module
* Vulnerability monitoring
* Docker deployment
* PostgreSQL migration

---

# Architecture Goal

The project is designed to provide:

* Better traceability of DSI processes
* Centralized technical documentation
* Improved audit readiness
* Secure role-based access management
* Scalable architecture for future extensions

---

## Contributors

- Sara Benbraham
- Farah Laggoune

## License

This repository is intended for educational and internship purposes.
