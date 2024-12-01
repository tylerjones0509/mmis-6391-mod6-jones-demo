from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

accounts = Blueprint('accounts', __name__)

@accounts.route('/account', methods=['GET', 'POST'])
def account():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new account
    if request.method == 'POST':
        account_name = request.form['account_name']

        # Insert the new account into the database
        cursor.execute('INSERT INTO accounts (account_name) VALUES (%s)', (account_name,))
        db.commit()

        flash('New account added successfully!', 'success')
        return redirect(url_for('accounts.account'))

    # Handle GET request to display all accounts
    cursor.execute('SELECT * FROM accounts')
    all_accounts = cursor.fetchall()
    return render_template('accounts.html', all_accounts=all_accounts)

@accounts.route('/update_account/<int:account_id>', methods=['GET', 'POST'])
def update_account(account_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the account's details
        account_name = request.form['account_name']

        cursor.execute('UPDATE accounts SET account_name = %s WHERE account_id = %s', (account_name, account_id))
        db.commit()

        flash('Account updated successfully!', 'success')
        return redirect(url_for('accounts.account'))

    # GET method: fetch account's current data for pre-populating the form
    cursor.execute('SELECT * FROM accounts WHERE account_id = %s', (account_id,))
    current_account = cursor.fetchone()
    return render_template('update_account.html', current_account=current_account)

@accounts.route('/delete_account/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the account
    cursor.execute('DELETE FROM accounts WHERE account_id = %s', (account_id,))
    db.commit()

    flash('Account deleted successfully!', 'danger')
    return redirect(url_for('accounts.account'))
