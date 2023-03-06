from flask import Flask, jsonify, request
import sqlite3
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


app = Flask(__name__)
CORS(app)

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

@app.route('/transactions/<int:transaction_id>')
def get_transaction(transaction_id):
    conn = sqlite3.connect('transactions.db')
    
    cursor = conn.execute('SELECT * FROM transactions WHERE id=?', (transaction_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row is None:
        return jsonify({'error': 'Transaction not found'}), 404
    
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
    
    return jsonify(transaction)
    
if __name__ == '__main__':
    app.run()
