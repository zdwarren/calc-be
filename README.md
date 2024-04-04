# Calculator App Backend

## Introduction

This repository contains the backend (BE) part of a simple calculator application. The backend is responsible for processing calculation requests sent from the frontend, evaluating mathematical expressions, and returning the results. It's built with Django and Django REST Framework (DRF) for a RESTful API and uses Celery for asynchronous task processing.

## Features

- **RESTful API**: Exposes endpoints for creating and fetching calculations.
- **Asynchronous Processing**: Utilizes Celery for handling calculation tasks asynchronously.
- **Security**: Implements basic checks to ensure only safe mathematical expressions are evaluated.

## Installation

Before starting, ensure you have Python and pip installed on your system. Then, follow these steps:

1. **Clone the Repository**

```bash
git clone https://github.com/zdwarren/calc-be.git
cd calc-be
```

2. **Create and Activate a Virtual Environment**

For Unix/macOS:
```bash
python3 -m venv env
source env/bin/activate
```
For Windows:
```bash
python -m venv env
.\env\Scripts\activate
```
3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Apply Migrations**
```bash
python manage.py migrate
```

5. **Run the Development Server**
```bash
python manage.py runserver
```

## Running Celery Worker

To process calculations asynchronously, you need to run a Celery worker alongside the development server. Open a new terminal, activate the virtual environment as shown above, and run:

```bash
celery -A calc_be worker --loglevel=info --pool=solo
```