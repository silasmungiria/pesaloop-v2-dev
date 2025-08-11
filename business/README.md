# PesaLoop

**PesaLoop** is a payment gateway and financial platform offering services such as fund transfers, wallet management, user authentication, credit and forex services, and more.  
The backend is powered by **Django** and **Celery**, while the frontend is built using **React Native**.

---

## 🚀 Features

- User authentication and RBAC
- Wallet and payment services
- Credit and forex modules
- Asynchronous task processing with Celery
- API documentation via Swagger and Redoc
- Modular service-based Django architecture

---

## 🛠️ Requirements

Ensure the following are installed before starting:

- Python 3.x
- pip (Python package installer)
- Redis (used by Celery as a broker/backend)
- Git

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/musiedgroup/pesaloop.git
cd pesaloop/business
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

- **Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file or set the following environment variables:

- `DATABASE_URL`
- `CELERY_BROKER_URL`
- `SECRET_KEY`
- `FRONTEND_URL`
- `APP_NAME`

Ensure **Redis** is running locally or accessible remotely.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

API Docs:

- Swagger: `/api/docs/swagger/`
- Redoc: `/api/docs/redoc/`

---

## ⏱️ Celery Task Queue

### Start a Celery Worker

- **Windows**:

  ```bash
  celery -A pesaloop.celery worker --loglevel=info --pool=solo
  ```

- **macOS/Linux**:

  ```bash
  celery -A pesaloop.celery worker --loglevel=info --pool=threads
  ```

### Run Celery Beat (Scheduled Tasks)

```bash
celery -A pesaloop beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l info
```

### Monitor with Flower

```bash
celery -A pesaloop flower
```

Access Flower at: [http://localhost:5555](http://localhost:5555)

```bash
celery -A pesaloop worker -l info
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🧭 Project Structure

```
.
├── authservice/           # User authentication
├── pesaloop/              # Project settings & root config
├── creditservice/         # Credit management
├── forexservice/          # Forex operations
├── integrations/          # External service integrations
├── mediaservice/          # Media/file handling
├── paymentservice/        # Payment processing
├── rbac/                  # Role-Based Access Control
├── reportingservice/      # Analytics & reporting
├── userservice/           # User profiles & logic
├── walletservice/         # Wallet management
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔐 Role-Based Access Control (RBAC)

### 1. Automatic Permission Registration

Permissions are auto-registered when:

- The server starts
- Migrations are run
- Views are added using `@register_permissions`

### 2. Manual Registration

```bash
python manage.py register_permissions
```

### 3. Decorators for Views

Add `@register_permissions` to class-based views.
Use attributes like `get_permission`, `post_permission`, etc.

### 4. Model-Level Permissions

Add `permission_basename` to models for CRUD permission generation.

---

## 📝 Notes

- Redis is required for Celery workers and Beat scheduler.
- SQLite is used by default in development; PostgreSQL recommended for production.
- React Native frontend consumes the backend APIs.

---

## 🧯 Troubleshooting

- ✅ Redis running?
- ✅ Celery worker and Beat active?
- ✅ Environment variables set?
- ✅ Logs checked for errors?

---

## 📄 License

This project is licensed under the **MIT License**.
See [LICENSE](../LICENSE.md) for full details.

---

## 📜 Terms & Conditions

By using this service, you agree to our [Terms & Conditions](../TERMS.md).
Please review them before proceeding.

---
