from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma =  Marshmallow(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=False)

    def __init__(self, title):
        self.title = title
class TodosSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title']

todo_schema = TodosSchema()
todos_schema = TodosSchema(many=True)

@app.route('/add', methods=['POST'])
@cross_origin()
def add_todo():

    title = request.json['title']

    new_todo = Todo(title)

    db.session.add(new_todo)
    db.session.commit()

    return todo_schema.jsonify(new_todo)


@app.route('/todo', methods=['GET'])
@cross_origin()
def get_todo():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

@app.route('/todo/<id>', methods=['GET'])
@cross_origin()
def get_todo_by_id(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)

@app.route('/todo/<id>', methods=['DELETE'])
@cross_origin()
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)



if __name__ == "__main__":
    app.run(debug=True)