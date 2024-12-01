from .db_connect import get_db


def get_portfolio_cost():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT SUM(t.quantity * t.price_paid) AS total_portfolio_value_cost
    FROM transactions t
    """
    cursor.execute(query)
    cost_result = cursor.fetchone()
    return cost_result['total_portfolio_value_cost'] if cost_result['total_portfolio_value_cost'] is not None else 0


# Do another one based off the current ticker price in the tickers table and the quantity in the transactions table
def get_portfolio_value():
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT
        SUM(t.quantity * ti.current_price) AS total_portfolio_value
    FROM
        transactions t
    JOIN
        tickers ti
    ON
        t.ticker_id = ti.ticker_id
    """
    cursor.execute(query)
    value_result = cursor.fetchone()
    return value_result['total_portfolio_value']
