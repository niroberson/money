from flask import Flask, request, session, g ,redirect, url_for, \
    abort, render_template, flash

from connect import Database

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
def query():
    if request.method == 'POST':
        return run_query(request.form['keyword'])

def run_query(keyword):



if __name__ == "__main__":
    app.run()