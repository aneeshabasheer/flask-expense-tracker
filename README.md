# 📊 Personal Expense Tracker

A full-stack, responsive web application built with **Flask**, **SQLAlchemy**, and **Bootstrap 5** that enables users to manage, categorize, and track their personal finances effectively.

---

## 🚀 Live Demo

- **Live Web Application:** [https://flask-expense-tracker.onrender.com](https://flask-expense-tracker.onrender.com)
- **Hosted On:** Render

---

## ✨ Features

- **User Authentication:** Secure signup, login, and session management using `Flask-Login` and password hashing (`Werkzeug`).
- **Expense Management:** Full CRUD capabilities (Create, Read, Update, Delete) for daily income and expense entries.
- **Categorization:** Classify transactions (e.g., Food, Rent, Salary, Entertainment) for clear spending insights.
- **Analytics & Dashboard:** Visual summaries and real-time computation of total balance, total income, and total expenses.
- **Responsive UI:** Clean, modern interface designed with Bootstrap 5 for desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite, SQLAlchemy ORM
- **Authentication:** Flask-Login
- **Production Server:** Gunicorn (v21.2.0)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2 Templates
- **Version Control & Hosting:** Git, GitHub, Render

---

## 📂 Project Structure

```text
flask-expense-tracker/
│
├── app.py              # Main application logic & route handlers
├── models.py           # Database models (User, Expense, Category)
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment process file for Render/Heroku
├── instance/
│   └── database.db     # SQLite database (local development)
├── templates/          # HTML templates (Jinja2)
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── static/             # Static assets (CSS, JS, images)
    ├── css/
    └── js/
```

---

## 💻 Local Setup & Installation

Follow these steps to set up and run the application locally on your machine:

### 1. Prerequisites
Ensure you have Python 3.8+ and Git installed:
```bash
python --version
git --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/aneeshabasheer/flask-expense-tracker.git
cd flask-expense-tracker
```

### 3. Create & Activate Virtual Environment
```bash
# On Windows (PowerShell / Git Bash)
python -m venv venv
source venv/Scripts/activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to view the app locally.

---

## 🚀 Deployment Notes

This application is deployed on **Render** using **Gunicorn**:
- **Start Command:** `gunicorn app:app`
- **Environment Variable:** Ensure `SECRET_KEY` is configured in production.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).