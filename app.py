from flask import Flask, render_template, request, redirect, url_for
from block import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        _from = request.form['from']
        to = request.form['to']
        amount = request.form['amount']
        write_block(_from, to, amount)
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/check', methods=['GET'])
def check():
    result = check_integrity()
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
