# CITS5505-Group29-Project
# CITS5505 Project - F1 Friends

## 📌 Description

🏁 **F1 Friends** is a Flask-based web application for Formula 1 enthusiasts to interact socially while predicting race outcomes.

It allows users to:

- 🧑‍💻 Register and select a favorite team & driver (→ `/register`)
- 📝 Edit their profile with avatar, bio, and team info (→ `/profile`, `/edit_profile`)
- 📊 Upload predictions and view visualized analytics (→ `/upload`, `/dashboard`)
- 📈 See real-time standings from the external F1 API (→ `/dashboard`)
- 🧑‍🤝‍🧑 Follow friends and chat privately (→ `/friends`)
- 🔒 Share prediction data selectively with mutual followers (→ sharing is handled through mutual-follow system)

This project fulfills the requirements of a **data analytics web application** by allowing private data uploads, automated analysis, and selective sharing options.

The following **required views** are implemented:

| View Type         | Path(s)             | Description |
|-------------------|---------------------|-------------|
| Intro view        | `/`                 | Application overview with login/register |
| Upload data view  | `/upload`           | Users upload predictions (private data) |
| Visualise data    | `/dashboard`        | Standings and prediction charts |
| Share data        | `/friends`          | Share access via mutual-follow |
| Login/Register    | `/login`, `/register` | User auth system |


---

## 👥 Team Members

| Group     | Name             | UWA ID    | GitHub Username     |
|-----------|------------------|-----------|----------------------|
| F1 Friends| Zoe Jin          | 24462297  | Megumi456           |
| F1 Friends| Chi Zhang        | 23954248  | MomobamiKiraly      |
| F1 Friends| Jean Wang        | 24137024  | unicorn-seer        |
| F1 Friends| Rabi Ul Hasan    | 23881368  | DueDiligence21      |

---

## 🔧 Recommended Environment

- **Python Version**: 3.11.x  
> ✅ We recommend using **Python 3.11** to ensure compatibility with dependencies and avoid known issues with async libraries and Flask extensions.

---

## 🚀 How to Run Locally

```bash
# Clone the repository and navigate to project root
git clone https://github.com/YOUR_USERNAME/CITS5505-Group29-Project.git
cd CITS5505-Group29-Project

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database (if first time)
flask db upgrade

# Run the server
flask run
```

---

## 🧪 How to Run Tests

This project includes both unit tests and Selenium UI tests.

### ✅ Unit Tests

```bash
pytest tests/test_unit.py
```

### ✅ Selenium Tests

Ensure the app is running locally at `http://127.0.0.1:5000`, then run:

```bash
pytest tests/test_selenium.py
```

> ℹ️ **Selenium WebDriver** (e.g., ChromeDriver) must be installed and in your PATH.

---

## 📦 Project Structure

```bash
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms/
│   ├── routes/
│   └── templates/
├── static/
├── tests/
│   ├── test_unit.py
│   └── test_selenium.py
├── requirements.txt
├── README.md
└── run.py
```

---

## 🔐 Security

- ✅ Passwords stored as salted hashes using Werkzeug.
- ✅ CSRF protection enabled via Flask-WTF.
- ✅ All forms include input validation and CSRF tokens.
- ✅ `.env` files used to manage secrets (and ignored via `.gitignore`)
- ✅ (Optional) Flask-Talisman can be added for HTTPS + secure headers.

---

## 🛠 Dependencies

All required packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

Frameworks & tools used:

- Flask + Flask-WTF + Flask-Migrate
- Bootstrap (for styling & responsiveness)
- SQLite (with SQLAlchemy ORM)
- Chart.js (for visualizing race standings and predictions)
- Selenium + Pytest (for testing)

---

## 📱 Mobile Support

All pages are built with **Bootstrap** and responsive layouts, ensuring a smooth experience on both desktop and mobile devices.

---

## 🧪 Demo Assets

- The file `app/static/charts/standings.png` is a pre-generated sample chart used for demo purposes on the dashboard.
- This file is usually dynamically created but included here to ensure proper rendering during presentation.
- It is listed in `.gitignore` to avoid unnecessary versioning changes in future commits.

---

## ✅ Final Notes

This project is built entirely within the scope of approved technologies for CITS5505:

- HTML, CSS, JS (Bootstrap)
- Flask + SQLAlchemy + Flask-WTF
- SQLite
- Chart.js, Selenium, and other non-core analytics libraries

All required views are implemented with intuitive routing and clear functionality:

- `index.html` serves as the **Intro View**
- `/upload` handles **Data Upload**
- `/dashboard` and `/profile` are used for **Data Visualization**
- The **Share View** is achieved via the mutual follow system on `/friends`, controlling who can see your data and chat with you
- `/login` and `/register` provide **Authentication**

All routes are protected, styled consistently, and integrated with CSRF protection, and tested with both unit and Selenium suites.

---

## 🔧 Optional Developer Script

To simplify testing, an optional helper script `create_test_user.py` is included.  
You can run this script once (after the database is initialized) to insert a test user for local login.

```bash
python create_test_user.py