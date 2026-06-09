# College Lost & Found Portal

A simple Flask web app for reporting lost items and managing reports through an admin panel.

## Features
- Students submit lost item reports with description, email, optional name, and location.
- Admin panel lists all reports and allows marking reports as resolved.
- Uses SQLite for persistent storage.

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open the app at `http://127.0.0.1:5000/`.

## Notes
- The SQLite database is created automatically on first run as `lost_and_found.db`.
- For production, replace `app.secret_key` with a secure value and disable debug mode.
