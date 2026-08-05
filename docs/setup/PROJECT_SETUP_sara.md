# ICOSNET DSI Platform

# Technical Development Guide

## Author

Sara Benbraham

## Date

03 August 2026

---

# 1. Project Overview

## Project Name

ICOSNET DSI Platform

## Objective

The objective of this project is to develop an internal platform for the DSI (Direction des Systèmes d’Information) to improve the traceability and management of internal processes.

The platform aims to centralize and historize:

* Application sheets management
* Generic accounts management
* Meeting traceability
* Hardware tracking
* Vulnerability monitoring

The project follows a modular architecture where each business domain is implemented as an independent Django application.

---

# 2. Repository Initialization

A GitHub repository was created.

Repository name:

```
Icosnet_Traceability_Platform
```

Project structure:

```
Icosnet_Traceability_Platform/

├── backend/
├── frontend/
├── docs/
├── README.md
└── .gitignore
```

---

# 3. Git Configuration

The following `.gitignore` file is recommended:

```
# Python
.venv/
__pycache__/
*.pyc

# Django
db.sqlite3
.env

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/
```

---

# 4. Backend Setup

## 4.1 Python Virtual Environment

A virtual environment was created in the project root.

Command:

```bash
python -m venv .venv
```

Activation using Git Bash:

```bash
source .venv/Scripts/activate
```

---

# 5. Django Installation

Django was installed inside the virtual environment.

Command:

```bash
pip install django
```

Dependencies were saved:

```bash
pip freeze > requirements.txt
```

---

# 6. Django Project Creation

The Django backend was created inside the `backend` folder.

Command:

```bash
django-admin startproject config backend
```

Generated structure:

```
backend/

├── config/
│
├── manage.py
│
└── requirements.txt
```

---

# 7. Initial Database Configuration

Initial Django migrations were executed.

Commands:

```bash
python manage.py makemigrations

python manage.py migrate
```

---

# 8. Django Applications Structure

The project follows a modular architecture.

Each business functionality is isolated inside a Django application.

Current structure:

```
backend/

├── apps/
│
│── users/
│
└── application_sheet/
│
├── config/
│
├── manage.py
│
└── requirements.txt
```

---

# 9. Users Application

A dedicated Django application was created:

```
users
```

Location:

```
backend/apps/users/
```

The application was registered in:

```
config/settings.py
```

Example:

```python
INSTALLED_APPS = [
    ...
    "apps.users",
]
```

---

# 10. Custom User Model

The default Django User model was replaced by a custom model to support future roles and permissions.

Model:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
```

Configuration:

```python
AUTH_USER_MODEL = "users.User"
```

The application label was configured as:

```python
class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    label = "users"
```

This allows Django to reference the model using:

```
users.User
```

---

# 11. Migration Issue Encountered

During development, Django generated:

```
InconsistentMigrationHistory
```

## Cause

The default Django authentication migrations were already applied before creating the custom User model.

## Solution

The following files were removed:

```
db.sqlite3
```

and generated migrations:

```
apps/users/migrations/
```

except:

```
__init__.py
```

Database recreation:

```bash
python manage.py makemigrations

python manage.py migrate
```

The issue was successfully resolved.

---

# 12. Current Backend Structure

```
backend/

├── apps/
│
├── users/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── __init__.py
│
├── application_sheet/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── config/
│
├── manage.py
│
└── requirements.txt
```

---

# 13. Application Sheet Module

The first business module implemented is:

```
Application Sheet
```

Purpose:

Centralize technical and functional information related to applications managed by the DSI.

---

# 14. Application Sheet Models

Implemented entities:

## FicheApplicative

Main entity representing an application.

Contains:

* Application name
* Application code
* Functional domain
* Criticality
* Description
* Status
* Responsible engineer
* Departments

---

## Contract

Stores contractual information:

* Supplier
* Annual budget
* External support
* Contract reference

---

## Infrastructure

Stores technical infrastructure information:

* Cloud / On-Premise
* Virtualization platform
* Servers
* Network information
* Database information

---

## UtilisateurAcces

Manages application access information:

* Target users
* User profiles
* Access channels

---

## Developpement

Stores development information:

* Development mode
* Source management
* CI/CD process
* Environments

---

## ModuleMetier

Stores business modules related to an application.

---

## Stockage

Manages storage information:

* Persistence
* Storage locations

---

## Integration

Manages integrations:

* Active Directory
* Messaging
* BI

---

## FluxApplication

Manages communication flows between applications.

---

## Sauvegarde

Stores backup information.

---

## Intervention

Stores application intervention history.

---

# 15. Business Validation Rules

Validation rules were implemented using Django `clean()` methods.

Examples:

## Infrastructure

Cloud infrastructure requires:

* Cloud type

Database server requires:

* Database server IP
* Database server name

---

## User Access

Rules:

* Target users are mandatory.
* At least one access channel is required.
* Access channels must belong to allowed choices.

---

## Development

Rules:

Internal development requires:

* Source management

At least one environment must be selected.

---

## Storage

Persistent storage requires:

* At least one storage location

---

## Integration

Active Directory integration requires:

* AD groups

BI integration requires:

* BI method

---

## Backup

Scheduled backup requires:

* Backup tool
* Recurrence
* Backup time
* Backup console

---

# 16. Manual Testing

Models were tested using Django Shell.

Command:

```bash
python manage.py shell
```

Tests performed:

* Application creation
* Engineer association
* Department association
* Contract creation
* Infrastructure validation
* Cloud validation
* On-Premise validation
* Access validation
* Development validation
* Storage validation
* Integration validation
* Backup validation
* Intervention validation

---

# 17. Django REST Framework

Django REST Framework was installed.

Command:

```bash
pip install djangorestframework
```

Added to:

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

---

# 18. REST API Implementation

The API layer uses:

* ModelSerializer
* ViewSet
* DefaultRouter

Files:

```
application_sheet/

├── serializers.py
├── views.py
└── urls.py
```

---

# 19. Available APIs

Base URL:

```
/api/
```

Example:

```
GET     /api/fiches/
POST    /api/fiches/
GET     /api/fiches/{id}/
PUT     /api/fiches/{id}/
DELETE  /api/fiches/{id}/
```

Other endpoints:

```
/api/contrats/

/api/infrastructures/

/api/acces/

/api/developpements/

/api/modules/

/api/stockages/

/api/integrations/

/api/flux/

/api/sauvegardes/

/api/interventions/
```

---

# 20. API Testing

APIs were tested using Django REST Framework interface.

Example:

```
http://127.0.0.1:8000/api/fiches/
```

Supported operations:

* GET
* POST
* PUT
* DELETE

---

# 21. Frontend Setup

## Technologies

Frontend:

* React
* Vite
* JavaScript
* ESLint

Required:

* Node.js LTS
* npm
* Visual Studio Code

---

# 22. Creating React Application

From project root:

```bash
npm create vite@latest frontend
```

Choose:

```
React
JavaScript
```

Move to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# 23. Frontend Launch

Command:

```bash
npm run dev
```

Frontend available at:

```
http://localhost:5173
```

---

# 24. Frontend Dependencies

Install:

React Router:

```bash
npm install react-router-dom
```

Axios:

```bash
npm install axios
```

React Icons:

```bash
npm install react-icons
```

SweetAlert2:

```bash
npm install sweetalert2
```

---

# 25. Frontend Architecture

Recommended structure:

```
src/

├── assets/

├── components/
│   ├── common/
│   ├── forms/
│   ├── layout/
│   └── tables/

├── pages/
│   ├── auth/
│   ├── dashboard/
│   ├── application_sheet/
│   ├── meetings/
│   └── profile/

├── services/

├── routes/

├── hooks/

├── context/

├── utils/

├── styles/

├── App.jsx

└── main.jsx
```

---

# 26. Backend / Frontend Communication

The frontend communicates with Django through REST APIs.

HTTP requests:

```
Axios
```

Because React and Django use different ports, CORS configuration will be added.

Required package:

```bash
pip install django-cors-headers
```

---

# 27. Current Development Status

Completed:

✅ GitHub repository
✅ Python environment
✅ Django initialization
✅ Custom User model
✅ Users application
✅ Application Sheet module
✅ Database models
✅ Relationships
✅ Business validations
✅ Django REST Framework
✅ REST APIs
✅ React + Vite initialization

---

# 28. Next Development Milestone

## Authentication and Authorization

Tasks:

* Extend User model
* Create roles:

```
Administrator
DSI
Department Head
Engineer
```

* Implement JWT authentication
* Configure permissions
* Protect API endpoints

---

# 29. Future Workflow

Application validation workflow:

```
Engineer

↓

Department Head

↓

DSI

↓

Validation / Rejection
```

---

# 30. Complete Commands History

```bash
python -m venv .venv

source .venv/Scripts/activate

pip install django

pip freeze > requirements.txt

django-admin startproject config backend

python manage.py makemigrations

python manage.py migrate

pip install djangorestframework

python manage.py shell

python manage.py runserver

npm create vite@latest frontend

npm install
```

---

# Final Notes

The project follows a scalable modular architecture.

Each business domain is isolated into a dedicated Django application.

The backend is prepared for frontend integration and future deployment using:

* PostgreSQL
* Docker
* CI/CD
* Production environment
