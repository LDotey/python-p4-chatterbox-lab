from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: returns an array of all messages as JSON, 
# ordered by created_at in ascending order.
# POST /messages: creates a new message with a body and username from params, 
# and returns the newly created post as JSON.
@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        all_messages = [message.to_dict() for message in Message.query.all()]
        # all_messages = [message.to_dict() for message in Message.query.filter_by(created_at=created_at).all]
        return make_response(all_messages, 200)
    elif request.method == 'POST':
        new_message = Message(
            body=request.json.get("body"),
            username=request.json.get("username"),
        )
        db.session.add(new_message)
        db.session.commit()
        new_message_dict = new_message.to_dict()

        response = make_response(new_message_dict, 201)

        return response

# PATCH /messages/<int:id>: updates the body of the message using params, 
# and returns the updated message as JSON.
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        return make_response(message_dict, 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {"delete successful": True,
                         "message": "Message deleted"}
        response = make_response(response_body, 200)

        return response

if __name__ == '__main__':
    app.run(port=5555)

# @app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
# def messages_by_id(id):
#     message = Message.query.filter_by(id=id).first()

#     if not message:
#         return make_response(
#             jsonify({"Error": "Message not found"}),
#             404
#         )

#     if request.method == 'PATCH':
#         # Use JSON input instead of form data
#         body = request.json.get("body")

#         if not body:
#             return make_response(
#                 jsonify({"error": "The 'body' parameter is required to update the message."}),
#                 400  # Bad Request if body is not provided
#             )

#         # Update message body
#         message.body = body
#         db.session.commit()

#         message_dict = message.to_dict()

#         response = make_response(
#             jsonify(message_dict),
#             200
#         )
#         return response

#     elif request.method == 'DELETE':
#         # Delete the message from the database
#         db.session.delete(message)
#         db.session.commit()

#         response_body = {
#             "delete_successful": True,
#             "message": "Message deleted."
#         }

#         response = make_response(
#             jsonify(response_body),
#             200
#         )
#         return response

# if __name__ == '__main__':
#     app.run(port=5555)
