from search import search
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def main():
    if request.method == 'POST':
        query = request.form['query']
        results = search(query)
        hits = results['hits']['hits']
        results_count = len(hits)
        aggs = results['aggregations']
        return render_template('index.html', hits=hits, results_count=results_count, que=' '.join(query).strip(),agg = aggs)
    if request.method == 'GET':
        return render_template('index.html',init='True')

if __name__ == '__main__':
    app.run(debug=True)
