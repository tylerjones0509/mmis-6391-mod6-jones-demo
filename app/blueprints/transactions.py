from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
from ..functions import get_portfolio_value


transactions = Blueprint('transactions', __name__)

@transactions.route('/transaction', methods=['GET', 'POST'])
def transaction():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new transaction
    if request.method == 'POST':
        transaction_date = request.form['transaction_date']
        quantity = request.form['quantity']
        price_paid = request.form['price_paid']
        ticker_id = request.form['ticker_id']
        account_id = request.form['account_id']

        # Insert the new transaction into the database
        cursor.execute(
            'INSERT INTO transactions (transaction_date, quantity, price_paid, ticker_id, account_id) VALUES (%s, %s, %s, %s, %s)',
            (transaction_date, quantity, price_paid, ticker_id, account_id)
        )
        db.commit()

        flash('New transaction added successfully!', 'success')
        return redirect(url_for('transactions.transaction'))

    # Handle GET request to display all transactions
    all_transactions = get_total_costs()
    total_portfolio_value = get_portfolio_value()

    # Fetch ticker symbols and account names for dropdowns
    cursor.execute('SELECT ticker_id, ticker_symbol FROM tickers')
    all_tickers = cursor.fetchall()

    cursor.execute('SELECT account_id, account_name FROM accounts')
    all_accounts = cursor.fetchall()

    return render_template('transactions.html',
                           all_transactions=all_transactions,
                           all_tickers=all_tickers,
                           all_accounts=all_accounts,
                           total_portfolio_value=total_portfolio_value)


@transactions.route('/update_transaction/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    db = get_db()
    cursor = db.cursor()

    # Update the transaction's details
    transaction_date = request.form['transaction_date']
    quantity = request.form['quantity']
    price_paid = request.form['price_paid']
    ticker_id = request.form['ticker_id']
    account_id = request.form['account_id']

    cursor.execute(
        'UPDATE transactions SET transaction_date = %s, quantity = %s, price_paid = %s, ticker_id = %s, account_id = %s WHERE transaction_id = %s',
        (transaction_date, quantity, price_paid, ticker_id, account_id, transaction_id)
    )
    db.commit()

    flash('Transaction updated successfully!', 'success')
    return redirect(url_for('transactions.transaction'))

@transactions.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the transaction
    cursor.execute('DELETE FROM transactions WHERE transaction_id = %s', (transaction_id,))
    db.commit()

    flash('Transaction deleted successfully!', 'danger')
    return redirect(url_for('transactions.transaction'))

####################################################
#####FUNCTIONS
####################################################

#Make a function that calculates the total cost of a transaction
def get_total_costs():
    db = get_db()  # Assumes get_db() is defined elsewhere and returns a database connection
    cursor = db.cursor()

    query = '''
    SELECT
        t.transaction_id,
        t.transaction_date,
        t.quantity,
        t.price_paid,
        t.ticker_id,
        t.account_id,
        tk.ticker_symbol,
        a.account_name,
        (t.quantity * t.price_paid) AS total_cost
    FROM transactions t
    JOIN tickers tk ON t.ticker_id = tk.ticker_id
    JOIN accounts a ON t.account_id = a.account_id
    ORDER BY
        t.transaction_date, 
        a.account_name;
    '''

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
###
def get_portfolio_value():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT SUM(t.quantity * t.price_paid) AS total_portfolio_value
    FROM transactions t
    """
    cursor.execute(query)
    result = cursor.fetchone()
    return result['total_portfolio_value']


