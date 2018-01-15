from flask import Flask, render_template, request, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = ":)"
mysql = MySQLConnector(app, "walldb")

def setup_session():
	if not "username" in session:
		session["username"] = None

@app.route("/")
def index():
	setup_session()
	messages = mysql.query_db("SELECT * FROM messages ORDER BY created_at DESC")

	return render_template("index.html", messages=messages)

@app.route("/login")
def login():
	setup_session()

	return render_template("login.html")

@app.route("/login/process", methods=["POST"])
def process_login():
	if True: #successful login
		setup_session()

		session["username"] = request.form["username"]

	return render_template("login.html", success=True)

@app.route("/logout")
def logout():
	session["username"] = None

	return render_template("index.html")

app.run(debug=True)