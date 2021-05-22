from flask import Flask, request, jsonify
from deta import Deta
from flask_cors import CORS

deta = Deta()

db = deta.Base("nusconnect")

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def getData():
    return jsonify(next(db.fetch()))

@app.route('/', methods=["POST"])
def postData():
    data = request.get_json()
    if data is None:
        return jsonify({"error":"Not in JSON format"})
    if 'id' not in data:
        return jsonify({"error":"No ID"})
    if 'modules' not in data:
        return jsonify({"error":"No modules"})
    if 'type' not in data:
        return jsonify({"error":"No type"})
    if 'question' not in data:
        return jsonify({"error":"No question"})
    if 'correct_answers' not in data:
        return jsonify({"error":"No correct answers"})
    if 'incorrect_answers' not in data:
        return jsonify({"error":"No incorrect answers"})
    result = db.put(request.json)
    return jsonify(result, 201)
