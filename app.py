from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from assistant import generate_reply
from database import init_db, create_user, get_user, add_reminder, list_reminders, log_conversation

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if get_user(username):
            return render_template("register.html", error="User already exists")
        user_id = create_user(username, generate_password_hash(password))
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(username)
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    message = data.get("message", "")
    user_id = session.get("user_id")

    result = generate_reply(message)
    reply_text = result["reply"] if isinstance(result, dict) else result

    if user_id:
        log_conversation(user_id, message, reply_text)

    return jsonify(result if isinstance(result, dict) else {"reply": reply_text})

@app.route("/api/reminders", methods=["POST"])
def api_add_reminder():
    data = request.get_json(force=True)
    add_reminder(
        data["user_id"],
        data["medicine"],
        data["reminder_time"],
        data.get("note", "")
    )
    return jsonify({"status": "ok"})

@app.route("/api/reminders/<int:user_id>")
def api_list_reminders(user_id):
    return jsonify(list_reminders(user_id))

if __name__ == "__main__":
    app.run(debug=True)
