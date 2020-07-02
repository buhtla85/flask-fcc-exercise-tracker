from flask import Flask, render_template, request, redirect, url_for, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
# init marshmallow - for serialization 
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    exercises = db.relationship('Exercise', backref='user')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# marshmallow schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

# init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/', methods=['GET', 'POST'])
def index():

    # if request.method == 'GET':
    #     pass
    if request.method == 'POST':
        return redirect(url_for('new_user'), code=307)

    return render_template('index.html')


@app.route('/api/exercise/new-user', methods=['POST'])
def new_user():
    new_name = request.form.get('name')
    if len(new_name) <= 1 and len(new_name) > 20:
        return 'Number of characters must be grater than 1 and less than 20.'
    else:
        new_username = User(name=new_name)
        try:
            db.session.add(new_username)
            db.session.commit()
            return user_schema.jsonify(new_username)
        except:
            return 'There was an issue adding user.'
    

# get all users from db and show them as json (as a list - [{id: mnmn, name: jghgjg}, {id: klkk, name: kjhjhj}, {}]) on this endpoint 
@app.route('/api/exercise/users', methods=['GET'])
def get_all_users():
    data = User.query.all()
    result = users_schema.dump(data)
    # obs - data prop on result object/dict!
    return jsonify(result)
    


# upon adding exercise we are being redirected to /api/exercise/add and the added exercise details are displayed in json format 


if __name__ == '__main__':
    app.run(debug=True)