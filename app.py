from flask import Flask, jsonify
import sqlite3
import json
from flask_cors import CORS


conn = sqlite3.connect('transactions.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    institution TEXT,
    account TEXT,
    merchant TEXT,
    amount REAL,
    type TEXT,
    categoryId INTEGER,
    category TEXT,
    isPending INTEGER,
    isTransfer INTEGER,
    isExpense INTEGER,
    isEdited INTEGER
);
''')

# Seed the transactions table
def seed_data():
    # Read data from the JSON file
    with open('temp_data.json') as f:
        data = json.load(f)

    # Connect to the database
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

    # Insert each transaction into the database
    for transaction in data:
        c.execute('''
            INSERT INTO transactions (date, institution, account, merchant, amount, type, categoryId, category, isPending, isTransfer, isExpense, isEdited)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction['date'],
            transaction['institution'],
            transaction['account'],
            transaction['merchant'],
            transaction['amount'],
            transaction['type'],
            transaction['categoryId'],
            transaction['category'],
            int(transaction['isPending']),
            int(transaction['isTransfer']),
            int(transaction['isExpense']),
            int(transaction['isEdited'])
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

seed_data()

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/transactions')
def get_transactions():
    conn = sqlite3.connect('transactions.db')
    
    cursor = conn.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    
    conn.close()
    
    transactions = []
    for row in rows:
        transaction = {
            'id': row[0],
            'date': row[1],
            'institution': row[2],
            'account': row[3],
            'merchant': row[4],
            'amount': row[5],
            'type': row[6],
            'categoryId': row[7],
            'category': row[8],
            'isPending': bool(row[9]),
            'isTransfer': bool(row[10]),
            'isExpense': bool(row[11]),
            'isEdited': bool(row[12])
        }
        transactions.append(transaction)
    
    return jsonify(transactions)

if __name__ == '__main__':
    app.run()
