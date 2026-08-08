# ICOSNET DSI Platform

## Description

**ICOSNET DSI Platform** is an internal web application developed for the Information Systems Department (DSI) to improve the traceability and management of internal IT processes.

The platform aims to centralize, structure, and historize important DSI activities such as:

* Application sheet management
* Generic account management
* Meeting traceability
* Hardware tracking

The project follows a modular Django architecture to ensure maintainability, scalability, and a clear separation between business modules.

---

# Technologies

## Backend

* Python
* Django
* SQLite (development)
* PostgreSQL (planned for production)

## Frontend

The user interface is implemented using **Django Templates** and standard HTML/CSS.

React and Vite are not used in the current architecture.

## Development Tools

* Git / GitHub
* Visual Studio Code
* Docker (planned)

---

# Project Structure

```text
Icosnet_Traceability_Platform/

├── backend/
│   ├── config/
│   │   └── ...
│   │
│   ├── apps/
│   │   ├── users/
│   │   ├── organization/
│   │   ├── application_sheet/
│   │   └── ...
│   │
│   ├── TEMPLATES/
│   │   ├── base.html
│   │   ├── application_sheet/
│   │   └── ...
│   │
│   ├── manage.py
│   └── ...
│
├── docs/
│
└── README.md
```

---

# Backend Architecture

The backend is organized using a modular Django architecture.

```text
backend/

├── apps/
│   ├── users/
│   │       # User and organizational roles
│   │
│   ├── organization/
│   │       # Organizational structure
│   │
│   └── application_sheet/
│           # Application Sheet business module
│
└── config/
        # Django project configuration
```

Each business functionality is implemented as an independent Django application.

This structure allows the platform to evolve by adding new modules without mixing their business logic.

---

# User Interface

The application uses Django's server-side rendering system.

The common interface is defined in:

```text
TEMPLATES/base.html
```

Application-specific templates are organized under:

```text
TEMPLATES/application_sheet/
```

The templates inherit from the common `base.html` template in order to maintain a consistent interface throughout the platform.

---

# Implemented Features

## Application Sheet Module

The first implemented business module is the **Application Sheet**.

It allows DSI teams to manage a complete application record containing several sections.

The main sections include:

* Application identification
* Contract information
* Infrastructure
* Users and access
* Development and configuration
* Business modules
* Storage
* Integrations
* Application flows
* Backup
* Interventions

The different sections are represented by dedicated Django models.

Each section is associated with the main `FicheApplicative` through a **One-to-One relationship**.

This ensures that a fiche has only one section of each type.

---

# Testing

The models and their relationships have been tested directly using the Django shell.

The tests include:

* Creation of an application sheet
* Creation of the different sections
* Verification of One-to-One relationships
* Validation using `full_clean()`
* Verification of required relationships
* Testing uniqueness constraints
* Verification that a second section of the same type cannot be associated with the same application sheet

For example, attempting to create a second `Intervention` for the same `FicheApplicative` correctly produces a uniqueness error.

This confirms that the One-to-One relationship is enforced both by Django validation and by the database constraint.

---

# Installation

## Clone the repository

```bash
git clone <repository_url>
cd Icosnet_Traceability_Platform
```

## Create the virtual environment

From the `backend` directory:

```bash
python -m venv .venv
```

## Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
python manage.py migrate
```

## Run the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

# Development Roadmap

Planned features include:

* Authentication and authorization
* Role and permission management
* Workflow validation system
* Generic accounts management
* Meeting traceability module
* Hardware tracking module
* Vulnerability monitoring
* PostgreSQL migration
* Docker deployment

---

# Architecture Goals

The project is designed to provide:

* Better traceability of DSI processes
* Centralized technical information
* Improved audit readiness
* Structured workflow management
* Clear separation of business modules
* Maintainable and scalable architecture
* Secure access management

---

## Contributors

* Sara Benbraham
* Farah Laggoune

---

## License

This repository is intended for educational and internship purposes.
