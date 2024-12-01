from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
from yfinance import Ticker
import pandas as pd
import matplotlib.pyplot as plt
import os

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

    # Handle GET request to display all tickers using Pandas
    cursor.execute('SELECT * FROM tickers')
    rows = cursor.fetchall()

    # Dynamically get column names from the cursor description
    columns = [desc[0] for desc in cursor.description]

    # Convert the fetched data to a Pandas DataFrame using dynamic columns
    df = pd.DataFrame(rows, columns=columns)

    # Convert DataFrame to a list of dictionaries to send to the template
    tickers_data = df.to_dict(orient='records')

    return render_template('tickers.html', all_tickers=tickers_data)

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

@tickers.route("/update_all_tickers", methods=["GET", "POST"])
def update_all_tickers():
    db = get_db()
    cursor = db.cursor()

    # Fetch all tickers from the database
    cursor.execute('SELECT * FROM tickers')
    all_tickers = cursor.fetchall()

    # Update the current price for each ticker
    for ticker in all_tickers:
        ticker_symbol = ticker['ticker_symbol']
        try:
            current_price = get_stock_price(ticker_symbol)
            cursor.execute(
                'UPDATE tickers SET current_price = %s WHERE ticker_symbol = %s',
                (current_price, ticker_symbol)
            )
        except Exception as e:
            flash(f'Failed to update {ticker_symbol}: {e}', 'danger')

    db.commit()
    flash('All tickers updated successfully!', 'success')
    return redirect(url_for('tickers.ticker'))



@tickers.route('/ticker_chart/<string:ticker_symbol>', methods=['GET'])
def ticker_chart(ticker_symbol):
    # Fetch historical data for the last day (with a 5-minute interval)
    ticker = Ticker(ticker_symbol)
    try:
        history = ticker.history(period='1d', interval='5m')
        if history.empty:
            flash(f'No data found for ticker symbol {ticker_symbol}.', 'danger')
            return redirect(url_for('tickers.ticker'))
    except Exception as e:
        flash(f'Failed to retrieve stock price for {ticker_symbol}: {str(e)}', 'danger')
        return redirect(url_for('tickers.ticker'))

    # Plotting the high and low prices throughout the day
    plot_path = os.path.join('app', 'static', 'images', f'{ticker_symbol}_high_low.png')
    plt.figure(figsize=(12, 6))
    plt.plot(history.index, history['High'], label='High Price', color='green')
    plt.plot(history.index, history['Low'], label='Low Price', color='red')
    plt.xlabel('Time')
    plt.ylabel('Prices')
    plt.title(f'High and Low Prices for {ticker_symbol} (Last Day)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    # Render template with chart
    return render_template('ticker_chart.html', ticker_symbol=ticker_symbol)

################################

# Function to get the latest stock price using yfinance
def get_stock_price(ticker_symbol):
    try:
        ticker = Ticker(ticker_symbol)
        history = ticker.history(period='1d')
        if not history.empty:
            return history['Close'].values[0]
        else:
            raise ValueError(f'No data found for ticker symbol {ticker_symbol}')
    except Exception as e:
        raise ValueError(f'Error retrieving stock price for {ticker_symbol}: {e}')
