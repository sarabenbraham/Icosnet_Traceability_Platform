# ICOSNET DSI Platform – Project Setup Report

## Author

Sara Benbraham

## Date

03 August 2026

---

# 1. Project Initialization

A new GitHub repository was created for the internship project.

Repository name:

```
Icosnet_Traceability_Platform
```

A Python virtual environment was created in the project root.

Command:

```bash
python -m venv .venv
```

Activation (Git Bash):

```bash
source .venv/Scripts/activate
```

---

# 2. Installing Django

Django was installed inside the virtual environment.

Command:

```bash
pip install django
```

Project dependencies were saved.

Command:

```bash
pip freeze > requirements.txt
```

---

# 3. Django Project Creation

A Django project was created inside the `backend` folder.

Command:

```bash
django-admin startproject config backend
```

Current structure:

```
Icosnet_Traceability_Platform/

backend/
│
├── config/
├── manage.py
└── requirements.txt
```

---

# 4. Initial Database

Default migrations were executed.

Commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 5. Users Application

A dedicated Django application named **users** was created.

Structure:

```
backend/
└── apps/
    └── users/
```

The application was registered inside `config/settings.py`.

```python
INSTALLED_APPS = [
    ...
    "apps.users",
]
```

---

# 6. Custom User Model

Instead of using Django's default User model, a custom user model was created to support future project requirements.

Current model:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
```

The project now uses this model through:

```python
AUTH_USER_MODEL = "users.User"
```

---

# 7. Users Application Configuration

`apps/users/apps.py`

```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    label = "users"
```

---

# 8. Migration Issue Encountered

During development, Django reported:

```
InconsistentMigrationHistory
```

Reason:

The default Django migrations had already been applied before introducing the custom User model.

Resolution:

* Deleted `db.sqlite3`
* Deleted generated migrations inside:

```
apps/users/migrations/
```

except

```
__init__.py
```

Then recreated the database.

Commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

Problem solved successfully.

---

# 9. Current Backend Structure

```
backend/

├── apps/
│   └── users/
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── views.py
│       └── __init__.py
│
├── config/
│
├── manage.py
│
└── requirements.txt
```

---

# 10. Development Status

Completed:

* GitHub repository
* Python virtual environment
* Django installation
* Backend initialization
* Django configuration
* Users application
* Custom User model
* Database migrations

Not started:

* Authentication
* Roles
* Dashboard
* Application Sheet module
* Meetings module
* Generic Accounts module
* Hardware Tracking module
* Vulnerability module
* Docker
* PostgreSQL
* API
* Frontend

---

# 11. Next Development Step

The next milestone is to implement the user management system.

Tasks:

* Extend the User model
* Introduce user roles:

  * Administrator
  * DSI
  * Department Head
  * Engineer
* Configure authentication
* Prepare permission management

Once the authentication layer is stable, development will continue with the **Application Sheet** module, which will be the first business module of the platform.

---

# Commands Executed

```bash
python -m venv .venv

source .venv/Scripts/activate

pip install django

pip freeze > requirements.txt

django-admin startproject config backend

python manage.py makemigrations

python manage.py migrate
```

Commands executed after introducing the custom user model:

```bash
python manage.py makemigrations

python manage.py migrate
```

---

# Notes

* The project follows a modular architecture.
* Each business feature will be implemented as a separate Django application.
* The project is intended to remain scalable and maintainable.
* Docker, PostgreSQL and deployment will be configured after the core application is functional.
