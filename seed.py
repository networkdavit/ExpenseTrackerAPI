import json
import sqlite3 

def seed_data():
    with open('temp_data.json') as f:
        data = json.load(f)

    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

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

    conn.commit()
    conn.close()

seed_data()