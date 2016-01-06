from flask import Flask, request, session, g ,redirect, url_for, \
    abort, render_template, send_from_directory

from factory import RecommenderFactory
from config import Config

DEBUG = False
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
    config = Config(DEBUG)

    keyword = None
    object = None
    predication = None

    if request.method == 'POST':
        # First search for subject
        try:
            keyword = request.form['keyword']
        except KeyError:
            error = 'No keyword entered or could be found'
            return render_template('query.html', error=error)

        # If a keyword is found, try to get a predication and object
        try:
            predication = request.form['predication']
        except KeyError:
            pass

        try:
            object = request.form['object']
        except KeyError:
            pass

        if object and predication:
            results = RecommenderFactory(config).search_concept_predication_object(keyword, predication, object)
            table = results.to_html()
            return render_template('query.html', keyword=keyword, predication=predication, object=object, results=table)
        elif object:
            results = RecommenderFactory(config).search_concept_object(keyword, object)
            table = results.to_html()
            return render_template('query.html', keyword=keyword, object=object, results=table)
        elif predication:
            results = RecommenderFactory(config).search_concept_predication(keyword, predication)
            table = results.to_html()
            return render_template('query.html', keyword=keyword, predication=predication, results=table)
        elif keyword:
            results = RecommenderFactory(config).search_concept(keyword)
            table = results.to_html()
            return render_template('query.html', keyword=keyword, results=table)

    return render_template('query.html')


@app.route('/graph', methods=['GET'])
def graph_viz():
    send_from_directory('static', filename='graph.json')
    return render_template('graph.html')


if __name__ == "__main__":
    app.run()
