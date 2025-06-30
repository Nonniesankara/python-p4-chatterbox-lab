from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/')
def index():
    return '<h1>Chatterbox API running</h1>'

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or "body" not in data or "username" not in data:
        abort(400, description="Missing body or username.")

    new_message = Message(
        body=data["body"],
        username=data["username"]
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        abort(404, description="Message not found.")

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]

    db.session.commit()

    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        abort(404, description="Message not found.")

    db.session.delete(message)
    db.session.commit()

    return '', 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
