from .db_connect import get_db


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