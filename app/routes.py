from flask import render_template
from . import app
from .functions import get_portfolio_value, get_portfolio_cost


@app.route('/')
def index():
    total_portfolio_value = get_portfolio_value()
    total_portfolio_costs = get_portfolio_cost()
    change = total_portfolio_value - total_portfolio_costs

    return render_template('index.html',
                           total_portfolio_value=total_portfolio_value,
                           total_portfolio_costs=total_portfolio_costs,
                           change=change)


@app.route('/about')
def about():
    return render_template('about.html')






