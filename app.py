import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func, extract
from models import db, User, Transaction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

CATEGORIES = [
    'Food', 'Travel', 'Shopping', 'Bills', 
    'Education', 'Health', 'Entertainment', 'Salary', 'Investment', 'Other'
]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- AUTHENTICATION ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered.', 'danger')
            return render_template('register.html')

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- APP ROUTES ---

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    # Calculate Summary Metrics
    income_total = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(
        user_id=current_user.id, type='income'
    ).scalar()

    expense_total = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(
        user_id=current_user.id, type='expense'
    ).scalar()

    balance = income_total - expense_total
    savings = max(0, balance)

    # Recent Transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())\
        .limit(5).all()

    return render_template(
        'dashboard.html',
        income_total=income_total,
        expense_total=expense_total,
        balance=balance,
        savings=savings,
        recent_transactions=recent_transactions
    )


@app.route('/transactions')
@login_required
def transactions():
    query = Transaction.query.filter_by(user_id=current_user.id)

    # Filter params
    category_filter = request.args.get('category')
    type_filter = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if category_filter:
        query = query.filter(Transaction.category == category_filter)
    if type_filter in ['income', 'expense']:
        query = query.filter(Transaction.type == type_filter)
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    transactions_list = query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()

    return render_template(
        'transactions.html',
        transactions=transactions_list,
        categories=CATEGORIES,
        selected_category=category_filter,
        selected_type=type_filter,
        start_date=start_date,
        end_date=end_date
    )


@app.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = request.form.get('amount')
        trans_type = request.form.get('type')
        category = request.form.get('category')
        trans_date = request.form.get('date')
        description = request.form.get('description', '').strip()

        if not amount or not trans_type or not category or not trans_date:
            flash('Please fill in all required fields.', 'danger')
            return render_template('transaction_form.html', categories=CATEGORIES, action="Add")

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            flash('Amount must be a positive number.', 'danger')
            return render_template('transaction_form.html', categories=CATEGORIES, action="Add")

        transaction = Transaction(
            amount=amount,
            type=trans_type,
            category=category,
            date=datetime.strptime(trans_date, '%Y-%m-%d').date(),
            description=description,
            user_id=current_user.id
        )

        db.session.add(transaction)
        db.session.commit()

        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))

    return render_template('transaction_form.html', categories=CATEGORIES, action="Add")


@app.route('/transaction/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        amount = request.form.get('amount')
        trans_type = request.form.get('type')
        category = request.form.get('category')
        trans_date = request.form.get('date')
        description = request.form.get('description', '').strip()

        if not amount or not trans_type or not category or not trans_date:
            flash('Please fill in all required fields.', 'danger')
            return render_template('transaction_form.html', categories=CATEGORIES, action="Edit", transaction=transaction)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            flash('Amount must be a positive number.', 'danger')
            return render_template('transaction_form.html', categories=CATEGORIES, action="Edit", transaction=transaction)

        transaction.amount = amount
        transaction.type = trans_type
        transaction.category = category
        transaction.date = datetime.strptime(trans_date, '%Y-%m-%d').date()
        transaction.description = description

        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions'))

    return render_template('transaction_form.html', categories=CATEGORIES, action="Edit", transaction=transaction)


@app.route('/transaction/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions'))


@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if full_name:
            current_user.full_name = full_name

        if new_password:
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return render_template('profile.html')
            current_user.set_password(new_password)

        db.session.commit()
        flash('Profile updated successfully!', 'success')

    return render_template('profile.html')


# --- API ENDPOINTS FOR CHARTS ---

@app.route('/api/chart-data')
@login_required
def chart_data():
    # 1. Expense Distribution by Category
    category_data = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter_by(user_id=current_user.id, type='expense')\
     .group_by(Transaction.category).all()

    categories = [c[0] for c in category_data]
    category_amounts = [float(c[1]) for c in category_data]

    # 2. Monthly Income vs Expense (Current Year)
    current_year = datetime.now().year
    
    monthly_income = db.session.query(
        extract('month', Transaction.date).label('month'),
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        extract('year', Transaction.date) == current_year
    ).group_by('month').all()

    monthly_expense = db.session.query(
        extract('month', Transaction.date).label('month'),
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        extract('year', Transaction.date) == current_year
    ).group_by('month').all()

    income_by_month = {int(m[0]): float(m[1]) for m in monthly_income}
    expense_by_month = {int(m[0]): float(m[1]) for m in monthly_expense}

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    income_series = [income_by_month.get(i, 0) for i in range(1, 13)]
    expense_series = [expense_by_month.get(i, 0) for i in range(1, 13)]

    return jsonify({
        'categories': {
            'labels': categories,
            'data': category_amounts
        },
        'monthly': {
            'labels': months,
            'income': income_series,
            'expense': expense_series
        }
    })


# Create DB tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)