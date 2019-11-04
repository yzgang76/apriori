from gzip1 import *
from sqlparse1 import *
from apriori2 import *
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/apriori')
def run():
    sqls = load_log_file()
    result = {}
    result1 = {}
    merged = {}
    for sc in sqls:
        parse(sc, result1)
        for k, v in result1.items():
            result[k] = [remove_duplication(v)]
        merged = merge_dict(merged, result)
        result = {}
        result1 = {}
    print(merged)
    # print()
    results = {}
    for k, v in merged.items():
        results[k] = run_apriori(v, 0.5, 0.7)
    # print()
    # print()
    print(results)
    return results


if __name__ == '__main__':
    app.run()
