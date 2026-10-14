# MailFlow — local Django email project

A beginner-friendly Django website with signup/login, a dashboard, a message composer, up to 10 recipients per batch, personalized greetings, and email history.

## Requirements
- Python 3.10 or newer
- VS Code (recommended)

## Run on Windows
Open this project folder in VS Code. Open **Terminal → New Terminal**, then run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations emailapp
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Local testing mode (default)
By default Django uses the console email backend. When you send an email, the message appears in the terminal where `runserver` is running. It is **not delivered to a real inbox**. The website stores each attempt in SQLite (`db.sqlite3`).

## Configure Gmail SMTP later (optional)
1. Enable 2-Step Verification on your Google account and create an App Password if your account supports it.
2. In the same terminal where you will run the server, set these environment variables (replace the sample values):

```powershell
$env:EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST="smtp.gmail.com"
$env:EMAIL_PORT="587"
$env:EMAIL_USE_TLS="True"
$env:EMAIL_HOST_USER="your-address@gmail.com"
$env:EMAIL_HOST_PASSWORD="your-google-app-password"
$env:DEFAULT_FROM_EMAIL="your-address@gmail.com"
python manage.py runserver
```

Never share or commit an actual app password. For a real deployment, replace the development `SECRET_KEY`, set `DEBUG=False`, configure allowed hosts, HTTPS, and secure environment-based secrets.

## How recipient input works
Enter one recipient per line:
```
Ravi, ravi@example.com
Priya, priya@example.com
```
The app sends each recipient a separate email with a personalized `Hi <name>` greeting. Tone is stored as a choice/label; it does not automatically rewrite your message. Review message content before sending.

## Notes
- SQLite is used to keep local setup simple; no separate SQL server is required.
- “Sent” in local mode means Django's console backend accepted the message and printed it to the terminal, not that it reached an inbox.
- This is a starter project for local learning, not a production-ready bulk email platform.
