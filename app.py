from flask import Flask, render_template, request, jsonify, redirect, url_for, json
from datetime import datetime

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # if request.method == 'GET':
    #     pass
    

    if request.method == 'POST':
        return redirect(url_for('new_user'), code=307)

    return render_template('index.html')


@app.route('/api/exercise/new-user', methods=['POST'])
def new_user():
    name = request.form.get('name')
    data = {"name": name} # data in JSON-serializable type
    response = app.response_class(response=json.dumps(data), status=200, mimetype='application/json')
    return response





if __name__ == '__main__':
    app.run(debug=True)