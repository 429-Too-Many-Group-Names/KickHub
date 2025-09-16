# Project-Generic-Software
A product-based software meant to be used to sell items online which would be shipped to customers. 

## Set up Virtual Environment
### Must be in the backend directory
python3 -m venv .venv
or
python -m venv .venv

## To activate virtual environment
. .venv/bin/activate

## Install all dependencies
pip install -r requirements

## .env for backend, add file in the root backend directory
GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID

GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET

MYSQL_HOST=localhost

MYSQL_USER=MYSQL_USER

MYSQL_PASSWORD=MYSQL_PASSWORD

MYSQL_DB=MYSQL_DB_NAME

## .env for the front end, add file in the root of frontend directory
VITE_GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID
