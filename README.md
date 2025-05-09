# CITS5505-Group29-Project 
# CITS5505 Project - F1 Predictor

## 📌 Description
A Flask web application allowing users to register, log in, update profile info (with avatar), and predict F1 results. Includes AI chatbot and SQLite backend.

---

## 🚀 How to Run

```bash
# Create and activate virtualenv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (if first time)
flask db upgrade

# Start server
flask run
```

---

## 🐍 Python 3.11 Setup (Minimal Dependencies)

If you're using **Python 3.11**, you can set up a minimal virtual environment:

```bash
python3.11 -m venv venv311
source venv311/bin/activate

# Install packages with system override (for environments like Kali Linux)
pip install --break-system-packages -r requirements-3.11.txt
```

### 📦 requirements-3.11.txt
```txt
Flask==3.1.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
Flask-WTF==1.2.2
WTForms==3.2.1
email-validator==2.1.1
openai==1.77.0
requests==2.32.3
matplotlib==3.10.1
pandas==2.2.3
```

---

## 🔄 Database Migrations (Flask-Migrate)

We use **Flask-Migrate** to manage database schema changes.

### 🛠 First-time setup for team members

After pulling the project for the first time, apply existing migrations with:

```bash
flask db upgrade
```

This will create tables like `user`, `prediction`, and `alembic_version`.

### 🧪 When you change any models

If you edit `models.py` (e.g., add a new field or table), run:

```bash
flask db migrate -m "Your change description"
flask db upgrade
```

> ⚠️ Important:
> - ❌ Do NOT use `db.create_all()` anymore.
> - ✅ Always commit changes to `migrations/` and `alembic.ini`.

---

## 🤝 Contributing

- Please follow the migration workflow above when changing database schema.
- Ensure your code passes basic manual testing before submitting PRs.

