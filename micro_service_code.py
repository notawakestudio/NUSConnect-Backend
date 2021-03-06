from flask import Flask, request, jsonify
from deta import Deta
from flask_cors import CORS

deta = Deta()

db_question = deta.Base("nusconnect")
db_quiz = deta.Base("nusconnect-quiz")
db_post = deta.Base("nusconnect-post")
db_reply = deta.Base("nusconnect-reply")
db_module = deta.Base("nusconnect-module")
db_user = deta.Base("nusconnect-user")

app = Flask(__name__)
CORS(app)


@app.route("/quiz/question/<questionId>", methods=["GET"])
def getQuestionById(questionId):
    return jsonify(db_question.get(questionId))


@app.route("/quiz/question", methods=["GET"])
def getAllQuestion():
    return jsonify(next(db_question.fetch()))


@app.route("/quiz/make", methods=["POST"])
def postQuestion():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "modules" not in data:
        return jsonify({"error": "No modules"})
    if "type" not in data:
        return jsonify({"error": "No type"})
    if "question" not in data:
        return jsonify({"error": "No question"})
    if "correct_answers" not in data:
        return jsonify({"error": "No correct answers"})
    if "incorrect_answers" not in data:
        return jsonify({"error": "No incorrect answers"})
    # use id received as key in deta base
    result = db_question.put(request.json, data["id"])
    return jsonify(result, 201)


@app.route("/quiz/quiz/<quizId>", methods=["GET"])
def getQuizById(quizId):
    return jsonify(db_quiz.get(quizId))


@app.route("/quiz/quiz", methods=["GET"])
def getAllQuiz():
    return jsonify(next(db_quiz.fetch()))


@app.route("/quiz/update", methods=["POST"])
def updateQuiz():
    data = request.get_json(force=True)
    db_quiz.put(data, data["id"])
    return "success"


@app.route("/quiz/collate", methods=["POST"])
def postQuiz():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "modules" not in data:
        return jsonify({"error": "No modules"})
    if "title" not in data:
        return jsonify({"error": "No title"})
    if "questions" not in data:
        return jsonify({"error": "No questions"})
    if "tags" not in data:
        return jsonify({"error": "No tags"})
    if "week" not in data:
        return jsonify({"error": "No week"})
    if "author" not in data:
        return jsonify({"error": "No author"})
    if "date" not in data:
        return jsonify({"error": "No date"})
    # use id received as key in deta base
    result = db_quiz.put(request.json, data["id"])
    return jsonify(result, 201)


#### FORUM STUFF ###################################


@app.route("/post/make", methods=["POST"])
def postPost():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "content" not in data:
        return jsonify({"error": "No content"})
    if "title" not in data:
        return jsonify({"error": "No title"})
    if "reply_count" not in data:
        return jsonify({"error": "No reply count"})
    if "tags" not in data:
        return jsonify({"error": "No tags"})
    if "week" not in data:
        return jsonify({"error": "No week"})
    if "author_id" not in data:
        return jsonify({"error": "No author"})
    if "created_date" not in data:
        return jsonify({"error": "No created date"})
    if "edited_date" not in data:
        return jsonify({"error": "No edited date"})
    if "up_votes" not in data:
        return jsonify({"error": "No up votes"})
    if "is_edited" not in data:
        return jsonify({"error": "No is edited"})
    # use id received as key in deta base
    result = db_post.put(request.json, data["id"])
    return jsonify(result, 201)


@app.route("/reply/make", methods=["POST"])
def postReply():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "post_id" not in data:
        return jsonify({"error": "No post_id"})
    if "author_id" not in data:
        return jsonify({"error": "No author_id"})
    if "content" not in data:
        return jsonify({"error": "No content"})
    if "created_date" not in data:
        return jsonify({"error": "No created_date"})
    if "edited_date" not in data:
        return jsonify({"error": "No edited_date"})
    if "up_votes" not in data:
        return jsonify({"error": "No up_votes"})
    if "is_edited" not in data:
        return jsonify({"error": "No is_edited"})
    # use id received as key in deta base
    result = db_reply.put(request.json, data["id"])
    return jsonify(result, 201)


@app.route("/forum/post", methods=["GET"])
def getAllPost():
    return jsonify(next(db_post.fetch()))


@app.route("/forum/reply", methods=["GET"])
def getAllReply():
    return jsonify(next(db_reply.fetch()))


@app.route("/forum/post/<postId>", methods=["GET"])
def getPostById(postId):
    return jsonify(db_post.get(postId))


@app.route("/post/update/<postId>", methods=["POST"])
def update_post(postId):
    data = request.get_json(force=True)
    post = db_post.update(data, postId)
    return data


@app.route("/post/update/<postId>", methods=["DELETE"])
def delete_post(postId):
    db_post.delete(postId)
    list_of_replies = list(next(db_reply.fetch({"post_id": postId})))
    for reply in list_of_replies:
        db_reply.delete(reply.get("id"))
    return "Deleted!"


@app.route("/forum/reply/<replyId>", methods=["GET"])
def getReplyById(replyId):
    return jsonify(db_reply.get(replyId))


@app.route("/forum/reply/related/<postId>", methods=["GET"])
def getRelatedRepliesByPostId(postId):
    return jsonify(next(db_reply.fetch({"post_id": postId})))


@app.route("/reply/update/<replyId>", methods=["POST"])
def update_reply(replyId):
    data = request.get_json(force=True)
    reply = db_reply.update(data, replyId)
    return reply


@app.route("/reply/update/<replyId>", methods=["DELETE"])
def delete_reply(replyId):
    db_reply.delete(replyId)
    return "DONE"


@app.route("/reply/update/likes/<replyId>", methods=["POST"])
def update_reply_likes(replyId):
    data = request.get_json(force=True)
    reply = db_reply.update(data, replyId)
    return "DONE"


@app.route("/post/update/likes/<postId>", methods=["POST"])
def update_post_likes(postId):
    data = request.get_json(force=True)
    post = db_post.update(data, postId)
    return "DONE"


#### MODULE STUFF ###################################


@app.route("/module/make", methods=["POST"])
def postModule():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "title" not in data:
        return jsonify({"error": "No title"})
    if "users" not in data:
        return jsonify({"error": "No users"})
    if "questions" not in data:
        return jsonify({"error": "No questions"})
    if "quizzes" not in data:
        return jsonify({"error": "No quizzes"})
    if "posts" not in data:
        return jsonify({"error": "No posts"})
    if "replies" not in data:
        return jsonify({"error": "No replies"})
    if "announcements" not in data:
        return jsonify({"error": "No announcements"})
    if "quests" not in data:
        return jsonify({"error": "No quests"})
    # use id received as key in deta base
    result = db_module.put(request.json, data["id"])
    return jsonify(result, 201)


@app.route("/module", methods=["GET"])
def getAllModule():
    return jsonify(next(db_module.fetch()))


@app.route("/module/<moduleId>", methods=["GET"])
def getModule(moduleId):
    return jsonify(db_module.get(moduleId))


@app.route("/module/addUser", methods=["POST"])
def addUserToModule():
    data = request.get_json(force=True)
    module = db_module.get(data.get("moduleId"))
    module["users"].append(data["userId"])
    db_module.put(module, data.get("moduleId"))

    user = db_user.get(data.get("userId"))
    user["modules"].append(data.get("moduleUserInfo"))
    db_user.put(user, data.get("userId"))
    return "success"


@app.route("/module/removeUser", methods=["POST"])
def removeUserFromModule():
    data = request.get_json(force=True)
    module = db_module.get(data.get("moduleId"))
    module["users"].remove(data["userId"])
    db_module.put(module, data.get("moduleId"))

    user = db_user.get(data.get("userId"))
    user["modules"] = [
        module for module in user["modules"] if module["id"] != data.get("moduleId")
    ]
    db_user.put(user, data.get("userId"))
    return "success"


@app.route("/module/announcement/make/<moduleId>", methods=["POST"])
def makeAnnoucement(moduleId):
    module = db_module.get(moduleId)
    data = request.get_json(force=True)
    currentAnnouncements = module.get("announcements")
    currentAnnouncements.append(data)
    db_module.put(module, moduleId)
    return "success"


@app.route(
    "/module/announcement/delete/<moduleId>/<announcementId>", methods=["DELETE"]
)
def deleteAnnoucement(moduleId, announcementId):
    module = db_module.get(moduleId)
    currentAnnouncements = module.get("announcements")
    module["announcements"] = [
        announcement
        for announcement in currentAnnouncements
        if announcement.get("id") != announcementId
    ]
    db_module.put(module, moduleId)
    return "success"


@app.route("/module/announcement/update/<moduleId>/<announcementId>", methods=["POST"])
def updateAnnoucement(moduleId, announcementId):
    data = request.get_json(force=True)
    module = db_module.get(moduleId)
    currentAnnouncements = module.get("announcements")
    module["announcements"] = [
        announcement
        for announcement in currentAnnouncements
        if announcement.get("id") != announcementId
    ]
    module["announcements"].append(data)
    db_module.put(module, moduleId)
    return "success"


@app.route("/module/quest/make/<moduleId>", methods=["POST"])
def makeQuest(moduleId):
    module = db_module.get(moduleId)
    data = request.get_json(force=True)
    currentQuests = module.get("quests")
    currentQuests.append(data)
    db_module.put(module, moduleId)
    return "success"


@app.route("/module/quest/delete/<moduleId>/<questId>", methods=["DELETE"])
def deleteQuest(moduleId, questId):
    module = db_module.get(moduleId)
    currentquests = module.get("quests")
    module["quests"] = [quest for quest in currentquests if quest.get("id") != questId]
    db_module.put(module, moduleId)
    return "success"


@app.route("/module/quest/update/<moduleId>/<questId>", methods=["POST"])
def updateQuest(moduleId, questId):
    data = request.get_json(force=True)
    module = db_module.get(moduleId)
    currentquests = module.get("quests")
    module["quests"] = [quest for quest in currentquests if quest.get("id") != questId]
    module["quests"].append(data)
    db_module.put(module, moduleId)
    return "success"


#### USER DATA STUFF ############


@app.route("/user/make", methods=["POST"])
def postUser():
    data = request.get_json(force=True)
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data:
        return jsonify({"error": "No ID"})
    if "modules" not in data:
        return jsonify({"error": "No modules"})
    if "profilePicUrl" not in data:
        return jsonify({"error": "No profilePicUrl"})
    if "role" not in data:
        return jsonify({"error": "No role"})
    if "userName" not in data:
        return jsonify({"error": "No string"})
    if "displayName" not in data:
        return jsonify({"error": "No displayName"})
    if "email" not in data:
        return jsonify({"error": "No email"})
    if "created_date" not in data:
        return jsonify({"error": "No created_date"})
    # use id received as key in deta base
    result = db_user.put(request.json, data["id"])
    return jsonify(result, 201)


@app.route("/user/<userId>", methods=["GET"])
def getUser(userId):
    return jsonify(db_user.get(userId))


@app.route("/user/check/<userId>", methods=["GET"])
def checkUserExists(userId):
    result = db_user.get(userId)
    if result is None:
        print("no such user")
        return jsonify({"exist": False})
    print("user exists")
    return jsonify({"exist": True})


@app.route("/user/update/<userId>", methods=["POST"])
def update_user(userId):
    data = request.get_json(force=True)
    updated = db_user.update(data, userId)
    return data


@app.route("/user/inbox/<userId>", methods=["GET"])
def getUserInbox(userId):
    user = db_user.get(userId)
    return jsonify(user["inbox"])


@app.route("/user/inbox/make/<userId>", methods=["POST"])
def submitToUserInbox(userId):
    user = db_user.get(userId)
    data = request.get_json(force=True)
    currentInbox = user.get("inbox")
    if not currentInbox:
        user["inbox"] = [data]
    else:
        user["inbox"].append(data)
    db_user.put(user, userId)
    return "success"


@app.route("/user/inbox/read/<userId>", methods=["POST"])
def markMessageAsRead(userId):
    user = db_user.get(userId)
    data = request.get_json(force=True)
    currentInbox = user.get("inbox")
    if not currentInbox:
        return "failed"
    for message in user["inbox"]:
        if message.get("id") == data.get("id"):
            message["read"] = True
    db_user.put(user, userId)
    return "success"


@app.route("/user/all", methods=["GET"])
def getAllUser():
    return jsonify(next(db_user.fetch()))
