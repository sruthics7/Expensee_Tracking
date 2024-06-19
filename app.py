from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Wallet Class
class Wallet:
    def __init__(self):
        self.balance = 0.0

    def add_money(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def deduct_money(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

# Category Class
class Category:
    def __init__(self):
        self.categories = []

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            return True
        return False

# Transaction Class
class Transaction:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, amount, category_name):
        transaction = {
            'amount': amount,
            'category': category_name,
            'date': datetime.date.today()
        }
        self.transactions.append(transaction)
        return transaction

# Report Class
class Report:
    def __init__(self, transactions):
        self.transactions = transactions

    def report_by_category(self):
        report = {}
        for transaction in self.transactions:
            category = transaction['category']
            amount = transaction['amount']
            if category in report:
                report[category] += amount
            else:
                report[category] = amount
        return report

    def report_by_month(self, month, year):
        report = {}
        for transaction in self.transactions:
            if transaction['date'].month == month and transaction['date'].year == year:
                date = transaction['date']
                amount = transaction['amount']
                if date in report:
                    report[date] += amount
                else:
                    report[date] = amount
        return report

    def report_by_day(self, day, month, year):
        report = {}
        for transaction in self.transactions:
            if transaction['date'] == datetime.date(year, month, day):
                category = transaction['category']
                amount = transaction['amount']
                if category in report:
                    report[category] += amount
                else:
                    report[category] = amount
        return report

# Initialize wallet, categories, and transactions
wallet = Wallet()
category = Category()
transaction = Transaction()

@app.route('/')
def index():
    return render_template('index.html', balance=wallet.balance, categories=category.categories, transactions=transaction.transactions)

@app.route('/add_money', methods=['POST'])
def add_money():
    amount = float(request.form['amount'])
    wallet.add_money(amount)
    return redirect(url_for('index'))

@app.route('/add_category', methods=['POST'])
def add_category():
    new_category = request.form['category']
    category.add_category(new_category)
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    category_name = request.form['category']
    if wallet.deduct_money(amount):
        transaction.add_transaction(amount, category_name)
    return redirect(url_for('index'))

@app.route('/report')
def report():
    report_type = request.args.get('type', 'category')
    if report_type == 'category':
        report_data = Report(transaction.transactions).report_by_category()
    elif report_type == 'monthly':
        month = int(request.args.get('month', datetime.date.today().month))
        year = int(request.args.get('year', datetime.date.today().year))
        report_data = Report(transaction.transactions).report_by_month(month, year)
    elif report_type == 'daily':
        day = int(request.args.get('day', datetime.date.today().day))
        month = int(request.args.get('month', datetime.date.today().month))
        year = int(request.args.get('year', datetime.date.today().year))
        report_data = Report(transaction.transactions).report_by_day(day, month, year)
    else:
        report_data = {}
    return render_template('report.html', report_data=report_data, report_type=report_type)

if __name__ == '__main__':
    app.run(debug=True)
