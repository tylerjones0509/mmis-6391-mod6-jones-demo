from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

tickers = Blueprint('tickers', __name__)

@tickers.route('/ticker', methods=['GET', 'POST'])
def ticker():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new ticker
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        current_price = request.form['current_price']

        # Insert the new ticker into the database
        cursor.execute('INSERT INTO tickers (ticker_symbol, current_price) VALUES (%s, %s)', (ticker_symbol, current_price))
        db.commit()

        flash('New ticker added successfully!', 'success')
        return redirect(url_for('tickers.ticker'))

    # Handle GET request to display all tickers
    cursor.execute('SELECT * FROM tickers')
    all_tickers = cursor.fetchall()
    return render_template('tickers.html', all_tickers=all_tickers)

@tickers.route('/update_ticker/<int:ticker_id>', methods=['GET', 'POST'])
def update_ticker(ticker_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the ticker's details
        ticker_symbol = request.form['ticker_symbol']
        current_price = request.form['current_price']

        cursor.execute('UPDATE tickers SET ticker_symbol = %s, current_price = %s WHERE ticker_id = %s', (ticker_symbol, current_price, ticker_id))
        db.commit()

        flash('Ticker updated successfully!', 'success')
        return redirect(url_for('tickers.ticker'))

    # GET method: fetch ticker's current data for pre-populating the form
    cursor.execute('SELECT * FROM tickers WHERE ticker_id = %s', (ticker_id,))
    current_ticker = cursor.fetchone()
    return render_template('update_ticker.html', current_ticker=current_ticker)

@tickers.route('/delete_ticker/<int:ticker_id>', methods=['POST'])
def delete_ticker(ticker_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the ticker
    cursor.execute('DELETE FROM tickers WHERE ticker_id = %s', (ticker_id,))
    db.commit()

    flash('Ticker deleted successfully!', 'danger')
    return redirect(url_for('tickers.ticker'))
