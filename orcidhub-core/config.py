# -*- coding: utf-8 -*-

"""Application configuration."""

from os import environ

authorization_base_url = 'https://sandbox.orcid.org/oauth/authorize'
token_url = 'https://pub.sandbox.orcid.org/oauth/token'
scope = ['/authenticate']

# Application redirect URL:
redirect_uri = "https://" + environ.get("ENV", "dev") + ".orcidhub.org.nz/auth"

# Database connection url
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD") or environ.get("PGPASSWORD") or "p455w0rd"

DATABASE_URL = environ.get("DATABASE_URL")

DB_NAME = environ.get("PGDATABASE", "orcidhub")
DB_USERNAME = environ.get("PGUSER", "orcidhub")
DB_PASSWORD = POSTGRES_PASSWORD
DB_HOSTNAME = environ.get("PGHOST", "db")

if not DATABASE_URL:
    from os import environ

# Orcid API client ID and secret
client_id = environ.get("ORCID_CLIENT_ID", "APP-TF7LKIE084PYTQ59")
client_secret = environ.get("ORCID_CLIENT_SECRET")

# Change the URL as per the enviornment
authorization_base_url = 'https://sandbox.orcid.org/oauth/authorize'
token_url = 'https://pub.sandbox.orcid.org/oauth/token'
scope = ['/authenticate']

# Application redirect URL:
redirect_uri = "https://" + environ.get("ENV", "dev") + ".orcidhub.org.nz/auth"

# Database connection url
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD") or environ.get("PGPASSWORD") or "p455w0rd"

DATABASE_URL = environ.get("DATABASE_URL")

DB_NAME = environ.get("PGDATABASE", "orcidhub")
DB_USERNAME = environ.get("PGUSER", "orcidhub")
DB_PASSWORD = POSTGRES_PASSWORD
DB_HOSTNAME = environ.get("PGHOST", "db")

if not DATABASE_URL:
    DATABASE_URL = "postgresql://" + DB_NAME
    if POSTGRES_PASSWORD:
        DATABASE_URL += ':' + POSTGRES_PASSWORD
    DATABASE_URL += "@" + DB_HOSTNAME + ":5432/" + DB_NAME

MAIL_USERNAME = environ.get("MAIL_USERNAME", "AKIAICSRSUE3LNBSIBVQ")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER", "no-reply@orcidhub.org.nz")
MAIL_SERVER = environ.get("MAIL_SERVER", "email-smtp.us-east-1.amazonaws.com")

TOKEN_PASSWORD_SALT = environ.get("TOKEN_PASSWORD_SALT")
TOKEN_SECRET_KEY = environ.get("TOKEN_SECRET_KEY")

MEMBER_API_FORM_BASE_URL = environ.get("MEMBER_API_FORM_BASE_URL",
                                       "https://orcid.org/content/register-client-application-sandbox")
NEW_CREDENTIALS = 'New_Credentials'
NOTE_ORCID = 'ORCID Hub integration for'
CRED_TYPE_PREMIUM = 2
APP_NAME = 'ORCID HUB'
APP_DESCRIPTION = 'We are having an ORCID integration through ORCID HUB New Zealand'
APP_URL = "https://" + environ.get("ENV", "dev") + ".orcidhub.org.nz"
