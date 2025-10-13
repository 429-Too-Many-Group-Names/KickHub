# Django App Setup Guide
---



## Prerequisites

- Python 3.10+ (https://www.python.org/downloads/)
- pip (comes with Python)
- git (optional, for cloning)
- sqlite3 (comes with Python standard library)


## 1. Clone the Repository




## 2. Set Up a Virtual Environment

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Database Setup (SQLite3)

- By default, Django uses `sqlite3` (file: `db.sqlite3`). No extra setup is needed.
- To inspect the database, use:

```bash
sqlite3 db.sqlite3
```

- To run SQL commands, use the SQLite prompt or a GUI tool (e.g., DB Browser for SQLite).

---

## 5. Django Migrations

Apply migrations to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
- Follow the prompts to set username, email, and password.
- Access the admin panel at: `http://127.0.0.1:8000/admin/`

---

## 7. Running the Development Server

```bash
python manage.py runserver
```
- Visit `http://127.0.0.1:8000/` in your browser.

---


## 8. Setting Up Google Authentication

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create/select a project.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth client ID**.
5. Choose **Web application**.
6. Set **Authorized redirect URIs** to:
   - `http://127.0.0.1:8000/accounts/google/login/callback/` (or your deployed URL)
7. Copy the **Client ID** and **Client Secret**.
8. Start your Django development server and log in to the Django admin panel at `http://127.0.0.1:8000/admin/`.
9. Go to the **Social Applications** section (usually under "Social Accounts" or "Social Apps").
10. Add a new Social Application for Google:
	- Enter your Client ID and Client Secret.
	- Select the correct site/domain.
	- Save the application.
11. No need to add these credentials to your settings file or `.env` if you use the admin interface.
12. Restart the server if needed.

---

## 9. Additional Notes

- **Static Files:**
	- Collect static files for production: `python manage.py collectstatic`
- **Environment Variables:**
	- Use a `.env` file or set variables in your shell for secrets and keys.
- **Requirements:**
	- If you add packages, run `pip freeze > requirements.txt` to update dependencies.
- **Deactivating venv:**
	- Run `deactivate` in your terminal.

---


## 10. Troubleshooting

- If you get `ModuleNotFoundError`, ensure your venv is activated and dependencies are installed.
- For database errors, try deleting `db.sqlite3` and rerunning migrations (note: this deletes all data).
- For Google Auth issues, double-check redirect URIs and credentials.
- If you see Django-related errors in the console (such as import errors, version mismatches, or missing packages), try running:
	- `pip uninstall django` (repeat for any problematic package)
	- `pip install -r requirements.txt`
	This can help resolve issues caused by conflicting or missing package versions.

---

## 11. Platform-Specific Tips

- **Windows:**
	- Use `python` instead of `python3`.
	- Use `venv\Scripts\activate` to activate the virtual environment.
- **Linux/macOS:**
	- Use `python3` and `source venv/bin/activate`.

---

## 12. Useful Commands

- Run tests: `python manage.py test`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`

---


## 13. Stripe API Integration (Coming Soon)

Stripe API integration for payment processing will be added soon. Stay tuned for updates and setup instructions!

### Stripe Documentation
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Python Integration Guide](https://stripe.com/docs/payments/accept-a-payment?platform=web&lang=python)
- [Stripe Django Integration Example](https://testdriven.io/blog/django-stripe/)

This guide will help you set up and run the Django app on Windows, Linux, and macOS. It covers prerequisites, virtual environments, dependencies, database setup, Google authentication, and admin configuration.

---

## 14. Further Reading & Documentation

- [Django Documentation (latest)](https://docs.djangoproject.com/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Settings & Environment Variables](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Django Database Setup](https://docs.djangoproject.com/en/stable/topics/db/)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Allauth (Social Auth)](https://django-allauth.readthedocs.io/en/latest/)

