from flask import Flask, request, session, g ,redirect, url_for, \
    abort, render_template, send_from_directory

from factory import RecommenderFactory

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    return render_template('query.html')


@app.route('/query', methods=['POST', 'GET'])
def submit_query():
    if request.method == 'POST':
        try:
            keyword = request.form['keyword']
        except KeyError:
            error = 'No keyword entered or could be found'
        results, error = RecommenderFactory(DEBUG).search_concept(keyword)
        if error:
            return render_template('query.html', keyword=keyword, error=error)
        else:
            table = results.to_html()
            return render_template('query.html', keyword=keyword, results=table)
    return render_template('query.html')


@app.route('/graph', methods=['GET'])
def graph_viz():
    send_from_directory('static', filename='graph-test.json')
    return render_template('graph.html')


if __name__ == "__main__":
    app.run()
