# Django App Setup Guide
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

## 13. Loading JSON Data into Django

To load JSON fixture files (such as sample data) into your Django database, use the `loaddata` management command. This is useful for populating your database with initial or sample data.

### Example

Suppose you have a file named `sample_data.json` in your app directory (e.g., `kickhub/sample_data.json`). Run:

```bash
python manage.py loaddata kickhub/sample_data.json
```

You can load multiple files or different fixtures as needed. Make sure your JSON files are formatted as Django fixtures.

**Django Fixture Documentation:**
- [Django Fixtures and loaddata](https://docs.djangoproject.com/en/stable/howto/initial-data/)



## 14. Stripe API Integration

This project uses Stripe for payment processing. Follow the steps below to set up Stripe integration locally.

### Step 1: Create a Stripe Account

1. Sign up for a free Stripe account at [https://stripe.com](https://stripe.com)
2. Navigate to the [Stripe Dashboard](https://dashboard.stripe.com/)
3. Switch to **Test Mode** (toggle in the top right corner)

### Step 2: Get Your API Keys

1. In the Stripe Dashboard, go to **Developers > API keys**
2. Copy your **Publishable key** and **Secret key** (test mode)
3. Keep these keys secure and never commit them to version control

### Step 3: Set Up Environment Variables

Create a `.env` file in your Django project root (or `django-app/` directory) with the following values:

```bash
# Stripe API Keys (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

**Important:**
- Replace the placeholder values with your actual Stripe keys
- The `STRIPE_WEBHOOK_SECRET` will be generated when you set up the Stripe CLI (see Step 4)
- Make sure `.env` is listed in your `.gitignore` file to prevent accidentally committing secrets

### Step 4: Install Stripe CLI

The Stripe CLI allows you to test webhooks locally by forwarding Stripe events to your development server.

#### **macOS**

Using Homebrew:
```bash
brew install stripe/stripe-cli/stripe
```

#### **Linux**

Using the installation script:
```bash
# Download and install
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
sudo apt update
sudo apt install stripe
```

Alternatively, download the binary directly:
```bash
# Download the latest release
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_linux_x86_64.tar.gz

# Extract and move to a directory in your PATH
tar -xvf stripe_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

#### **Windows**

Using Scoop:
```powershell
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
scoop install stripe
```

Or download the executable directly:
1. Download the latest Windows release from [GitHub Releases](https://github.com/stripe/stripe-cli/releases)
2. Extract the `stripe.exe` file
3. Add the directory containing `stripe.exe` to your system PATH

### Step 5: Authenticate Stripe CLI

After installation, authenticate the CLI with your Stripe account:

```bash
stripe login
```

This will open a browser window to authorize the CLI. Press Enter to confirm.

### Step 6: Forward Webhooks to Your Local Server

Start the Stripe webhook forwarding to listen for events and forward them to your local Django server:

```bash
stripe listen --forward-to localhost:8000/webhooks/stripe/
```

**Important:** Copy the webhook signing secret (`whsec_...`) that appears in the terminal and add it to your `.env` file as `STRIPE_WEBHOOK_SECRET`.

Example output:
```
> Ready! Your webhook signing secret is whsec_1234567890abcdef (^C to quit)
```

Keep this terminal window open while developing. The CLI will forward all Stripe events to your local server.

### Step 7: Test Your Integration

With your Django server running and the Stripe CLI listening, you can test payments using Stripe's test card numbers:

- **Successful payment:** `4242 4242 4242 4242`
- **Requires authentication:** `4000 0025 0000 3155`
- **Declined payment:** `4000 0000 0000 9995`

Use any future expiration date, any 3-digit CVC, and any postal code.

### Step 8: Trigger Test Events (Optional)

You can manually trigger test webhook events using the Stripe CLI:

```bash
# Trigger a successful payment event
stripe trigger payment_intent.succeeded

# Trigger a checkout session completed event
stripe trigger checkout.session.completed
```

### Stripe Documentation
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Python Integration Guide](https://stripe.com/docs/payments/accept-a-payment?platform=web&lang=python)
- [Stripe Django Integration Example](https://testdriven.io/blog/django-stripe/)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Stripe Test Cards](https://stripe.com/docs/testing)

This guide will help you set up and run the Django app on Windows, Linux, and macOS. It covers prerequisites, virtual environments, dependencies, database setup, Google authentication, and admin configuration.



---

## 15. Everything in Docker

This project is intended to be run entirely inside Docker. Use the commands below from your host shell; they will execute inside the running container named `superuser` (replace `superuser` with your service/container name if different).

1. Start the containers (foreground, rebuild if needed):

```bash
docker compose up --watch
or
docker compose up --build --watch
```

2. In a new terminal, run management commands inside the container. Examples:

```bash

# create a superuser (interactive)
docker exec -it < container_ID or name > python manage.py createsuperuser

# load JSON fixtures
docker exec superuser python manage.py loaddata kickhub/sample_data.json

# open a shell inside the container
docker exec -it < container name or id > bash
```

Notes:
- If your compose service/container has a different name, replace `superuser` with the actual container name shown by `docker ps`.
- You can run multiple Django commands in one exec using `sh -c "cmd1 && cmd2"`.

## 16. Further Reading & Documentation

- [Django Documentation (latest)](https://docs.djangoproject.com/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Settings & Environment Variables](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Django Database Setup](https://docs.djangoproject.com/en/stable/topics/db/)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Allauth (Social Auth)](https://django-allauth.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)




