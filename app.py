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

#db schemas
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    exercises = db.relationship('Exercise', backref='user')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# marshmallow schemas
# schema for returning {name: "", id: ""} /api/exercise/new-user
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

#schema for returning {id: "", username: "", date: "", duration: x, description: ""} /api/exercise/add
class AddExerciseToUserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'date', 'duration', 'description')

#nested "log" schema 
class LogSchema(ma.Schema):
    class Meta: 
        fields = ('description', 'duration', 'date')

#schema for returning {id: "", name:"", count: x, log: [{description: "", duration: x, date: ""}, {...}]}
class UserAndExercisesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'count', 'log')
        log = ma.List(ma.Nested(LogSchema, many=True))

# init schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
add_single_exercise = AddExerciseToUserSchema()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form['action'] == 'user':
        return redirect(url_for('new_user'), code=307)
    elif request.method == 'POST' and request.form['action'] == "exercise":
        return redirect(url_for('add_exercise'), code=307)
    else: 
        return render_template('index.html')

#add new user
#this route works
@app.route('/api/exercise/new-user', methods=['POST'])
def new_user():
    new_name = request.form['name']
    if len(new_name) <= 1 or len(new_name) > 20:
        return 'Number of characters must be grater than 1 and less than 20.'
    else:
        new_username = User(name=new_name)
        try:
            db.session.add(new_username)
            db.session.commit()
            return user_schema.jsonify(new_username)
        except:
            return 'There was an issue adding user.'
    

# get all users from db and return them to the user in json format (list - [{id: mnmn, name: jghgjg}, {id: klkk, name: kjhjhj}, {}])
# this route works and returns the expected json format 
@app.route('/api/exercise/users', methods=['GET'])
def get_all_users():
    data = User.query.all()
    result = users_schema.dump(data)
    return jsonify(result)


# add exercise and return them to the user in json format
@app.route('/api/exercise/add', methods=['POST'])
def add_exercise():
    user_id = request.form['userId']
    num_user_id = int(float(user_id))

    description = request.form['description']
    duration = request.form['duration']
    time = request.form['date']
    time_old = time.replace('T', ' ')
    time_new = datetime.strptime(time_old, '%Y-%m-%d')

    num_duration = int(float(duration))


    # if len(user_id) == 0 or len(description) == 0 or len(duration) == 0:
    #     return 'All fields are required.'
    # elif not verifiy_userID:
    #     return 'Invalid id.'
    # else:
    exercise_data = Exercise(description=description, duration=num_duration, date=time_new, user_id=num_user_id)
        
    db.session.add(exercise_data)
    db.session.commit()
    return add_single_exercise.jsonify(exercise_data)
        
            # return 'There was an issue adding user.'




if __name__ == '__main__':
    app.run(debug=True)