from flask import Flask, request, session, g ,redirect, url_for, \
    abort, render_template, flash

from connect import Database
from ReccomenderFactory import RecommenderFactory

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = Database().connect_local()


@app.route('/')
def home():
    return render_template('query.html')

@app.route('/query', methods=['POST', 'GET'])
def run_query():
    if request.method == 'POST':
        try:
            keyword = request.form['keyword']
        except KeyError:
            error = 'No keyword entered or could be found'
        # return run_query(request.form['keyword'])
        # results = RecommenderFactory().search_keyword(keyword)
        return render_template('query.html', keyword=keyword)
    return render_template('query.html')

if __name__ == "__main__":
    app.run()