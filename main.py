from flask import Flask, request, jsonify
from deta import Deta
from flask_cors import CORS

deta = Deta()

db_question = deta.Base("nusconnect")
db_quiz = deta.Base("nusconnect-quiz")

app = Flask(__name__)
CORS(app)

@app.route('/quiz/question/<questionId>', methods=["GET"])
def getQuestionById(questionId):
    return jsonify(db_question.get(questionId))

@app.route('/quiz/question', methods=["GET"])
def getAllQuestion():
    return jsonify(next(db_question.fetch()))

@app.route('/quiz/make', methods=["POST"])
def postQuestion():
    data = request.get_json(force=True)
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
    # use id received as key in deta base
    result = db_question.put(request.json, data['id'])
    return jsonify(result, 201)

@app.route('/quiz/quiz/<quizId>', methods=["GET"])
def getQuizById(quizId):
    return jsonify(db_quiz.get(quizId))

@app.route('/quiz/quiz', methods=["GET"])
def getAllQuiz():
    return jsonify(next(db_quiz.fetch()))


@app.route('/quiz/collate', methods=["POST"])
def postQuiz():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error":"Not in JSON format"})
    if 'id' not in data:
        return jsonify({"error":"No ID"})
    if 'modules' not in data:
        return jsonify({"error":"No modules"})
    if 'title' not in data:
        return jsonify({"error":"No title"})
    if 'questions' not in data:
        return jsonify({"error":"No questions"})
    if 'tags' not in data:
        return jsonify({"error":"No tags"})
    if 'week' not in data:
        return jsonify({"error":"No week"})
    if 'author' not in data:
        return jsonify({"error":"No author"})
    if 'date' not in data:
        return jsonify({"error":"No date"}) 
    # use id received as key in deta base
    result = db_quiz.put(request.json, data['id'])
    return jsonify(result, 201)

