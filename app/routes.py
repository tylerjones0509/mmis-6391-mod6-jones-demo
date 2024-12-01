from flask import render_template
from . import app
from .functions import get_portfolio_value


@app.route('/')
def index():
    total_portfolio_value = get_portfolio_value()
    return render_template('index.html', total_portfolio_value=total_portfolio_value)


@app.route('/about')
def about():
    return render_template('about.html')



