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


@app.route("/quiz/question/<moduleId>/<questionId>", methods=["GET"])
def getQuestionById(moduleId, questionId):
    questions = db_module.get(moduleId).get("questions")
    question = list(
        filter(lambda question: question.get("id") == questionId, questions)[0]
    )
    return jsonify(question)


@app.route("/quiz/question", methods=["GET"])
def getAllQuestion():
    return jsonify(next(db_question.fetch()))


@app.route("/quiz/question/all/<moduleId>", methods=["GET"])
def getAllQuestionByModule(moduleId):
    questions = db_module.get(moduleId).get("questions")
    return jsonify(questions)


@app.route("/quiz/make", methods=["POST"])
def postQuestion():
    data = request.get_json(force=True)
    question = data.get("question")
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in question:
        return jsonify({"error": "No ID"})
    if "modules" not in question:
        return jsonify({"error": "No modules"})
    if "type" not in question:
        return jsonify({"error": "No type"})
    if "question" not in question:
        return jsonify({"error": "No question"})
    if "correct_answers" not in question:
        return jsonify({"error": "No correct answers"})
    if "incorrect_answers" not in question:
        return jsonify({"error": "No incorrect answers"})
    module = db_module.get(data.get("moduleId"))
    questions = module.get("questions")
    questions.append(question)
    module["questions"] = questions
    result = db_module.put(module, module["id"])
    return jsonify(result, 201)


@app.route("/quiz/quiz/<quizId>", methods=["GET"])
def getQuizById(quizId):
    return jsonify(db_quiz.get(quizId))


@app.route("/quiz/quiz", methods=["GET"])
def getAllQuiz():
    return jsonify(next(db_quiz.fetch()))


@app.route("/quiz/all/<moduleId>", methods=["GET"])
def getAllQuizByModule(moduleId):
    quizzes = db_module.get(moduleId).get("quizzes")
    return jsonify(quizzes)


@app.route("/quiz/update", methods=["POST"])
def updateQuiz():
    data = request.get_json(force=True)
    module = db_module.get(data.get("moduleId"))
    quizzes = module.get("quizzes")
    quizzes = list(
        filter(lambda quiz: quiz.get("id") != data.get("quiz").get("id"), quizzes)
    )
    quizzes.append(data.get("quiz"))
    module["quizzes"] = quizzes
    db_module.update(module, module["id"])
    return "success"


@app.route("/quiz/collate", methods=["POST"])
def postQuiz():
    data = request.get_json(force=True)
    quiz = data.get("quiz")
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in quiz:
        return jsonify({"error": "No ID"})
    if "modules" not in quiz:
        return jsonify({"error": "No modules"})
    if "title" not in quiz:
        return jsonify({"error": "No title"})
    if "questions" not in quiz:
        return jsonify({"error": "No questions"})
    if "tags" not in quiz:
        return jsonify({"error": "No tags"})
    if "week" not in quiz:
        return jsonify({"error": "No week"})
    if "author" not in quiz:
        return jsonify({"error": "No author"})
    if "date" not in quiz:
        return jsonify({"error": "No date"})
    module = db_module.get(data.get("moduleId"))
    quizzes = module.get("quizzes")
    quizzes.append(quiz)
    module["quizzes"] = quizzes
    result = db_module.put(module, module["id"])
    return jsonify(result, 201)


#### FORUM STUFF ###################################


@app.route("/post/make", methods=["POST"])
def postPost():
    data = request.get_json(force=True)
    moduleId = data.get("moduleId")
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data["post"]:
        return jsonify({"error": "No ID"})
    if "content" not in data["post"]:
        return jsonify({"error": "No content"})
    if "title" not in data["post"]:
        return jsonify({"error": "No title"})
    if "reply_count" not in data["post"]:
        return jsonify({"error": "No reply count"})
    if "tags" not in data["post"]:
        return jsonify({"error": "No tags"})
    if "week" not in data["post"]:
        return jsonify({"error": "No week"})
    if "author_id" not in data["post"]:
        return jsonify({"error": "No author"})
    if "created_date" not in data["post"]:
        return jsonify({"error": "No created date"})
    if "edited_date" not in data["post"]:
        return jsonify({"error": "No edited date"})
    if "up_votes" not in data["post"]:
        return jsonify({"error": "No up votes"})
    if "is_edited" not in data["post"]:
        return jsonify({"error": "No is edited"})
    # use id received as key in deta base
    module = db_module.get(moduleId)
    posts = module.get("posts")
    posts.append(data["post"])
    module["posts"] = posts
    print("hello")
    db_module.put(module, data.get("moduleId"))
    return "DONE"


@app.route("/reply/make", methods=["POST"])
def postReply():
    data = request.get_json(force=True)
    moduleId = data.get("moduleId")
    if data is None:
        return jsonify({"error": "Not in JSON format"})
    if "id" not in data["reply"]:
        return jsonify({"error": "No ID"})
    if "post_id" not in data["reply"]:
        return jsonify({"error": "No post_id"})
    if "author_id" not in data["reply"]:
        return jsonify({"error": "No author_id"})
    if "content" not in data["reply"]:
        return jsonify({"error": "No content"})
    if "created_date" not in data["reply"]:
        return jsonify({"error": "No created_date"})
    if "edited_date" not in data["reply"]:
        return jsonify({"error": "No edited_date"})
    if "up_votes" not in data["reply"]:
        return jsonify({"error": "No up_votes"})
    if "is_edited" not in data["reply"]:
        return jsonify({"error": "No is_edited"})
    module = db_module.get(moduleId)
    replies = module.get("replies")
    replies.append(data["reply"])
    module["replies"] = replies
    db_module.put(module, data.get("moduleId"))
    return "DONE"


@app.route("/forum/post/<moduleId>", methods=["GET"])
def getAllPost(moduleId):
    posts = db_module.get(moduleId).get("posts")
    return jsonify(posts)


@app.route("/forum/reply", methods=["GET"])
def getAllReply():
    return jsonify(next(db_reply.fetch()))


@app.route("/forum/post/<moduleId>/<postId>", methods=["GET"])
def getPostById(moduleId, postId):
    posts = db_module.get(moduleId).get("posts")
    post = next((item for item in posts if item["id"] == postId), None)
    return jsonify(post)


@app.route("/post/update/<postId>", methods=["POST"])
def update_post(postId):
    data = request.get_json(force=True)
    module = db_module.get(data.get("moduleId"))
    posts = module.get("posts")
    for post in posts:
        if post["id"] == postId:
            for key, val in data.get("post").items():
                post[key] = val
    module["posts"] = posts
    db_module.put(module, data.get("moduleId"))
    return "DONE"


@app.route("/post/delete/<moduleId>/<postId>", methods=["DELETE"])
def delete_post(moduleId, postId):
    module = db_module.get(moduleId)
    replies = module.get("replies")
    posts = module.get("posts")
    module["replies"] = list(filter(lambda reply: reply["post_id"] == postId, replies))
    module["posts"] = list(filter(lambda post: post["id"] != postId, posts))
    db_module.put(module, moduleId)
    return "Deleted!"


@app.route("/forum/reply/<replyId>", methods=["GET"])
def getReplyById(replyId):
    return jsonify(db_reply.get(replyId))


@app.route("/forum/reply/related/<moduleId>/<postId>", methods=["GET"])
def getRelatedRepliesByPostId(moduleId, postId):
    replies = db_module.get(moduleId).get("replies")
    return jsonify(list(filter(lambda reply: reply["post_id"] == postId, replies)))


@app.route("/reply/update/<replyId>", methods=["POST"])
def update_reply(replyId):
    data = request.get_json(force=True)
    moduleId = data.get("moduleId")
    module = db_module.get(moduleId)
    replies = module.get("replies")
    for reply in replies:
        if reply.get("id") == replyId:
            for key, val in data.get("post").items():
                reply[key] = val
    module["replies"] = replies
    db_module.put(module, moduleId)
    return "DONE"


@app.route("/reply/delete/<moduleId>/<replyId>", methods=["DELETE"])
def delete_reply(moduleId, replyId):
    module = db_module.get(moduleId)
    replies = module.get("replies")
    module["replies"] = list(filter(lambda reply: reply["id"] != replyId, replies))
    db_module.update(module, moduleId)
    return "DONE"


@app.route("/reply/update/likes/<replyId>", methods=["POST"])
def update_reply_likes(replyId):
    data = request.get_json(force=True)
    moduleId = data.get("moduleId")
    module = db_module.get(moduleId)
    replies = module.get("replies")
    for reply in replies:
        if reply.get("id") == replyId:
            reply["up_votes"] = data.get("reply").get("up_votes")
    module["replies"] = replies
    db_module.put(module, moduleId)
    return "DONE"


@app.route("/post/update/likes/<postId>", methods=["POST"])
def update_post_likes(postId):
    data = request.get_json(force=True)
    moduleId = data.get("moduleId")
    module = db_module.get(moduleId)
    posts = module.get("posts")
    for post in posts:
        if post.get("id") == postId:
            post["up_votes"] = data.get("post").get("up_votes")
    module["posts"] = posts
    post = db_module.put(module, moduleId)
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
