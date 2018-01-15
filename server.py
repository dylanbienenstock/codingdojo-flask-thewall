from flask import Flask, render_template, request, session
from mysqlconnection import MySQLConnector
import os, md5, binascii, datetime

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

################## LOG IN ##################

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

################## REGISTRATION ##################

@app.route("/register")
def register():
	setup_session()

	return render_template("register.html")

@app.route("/register/process", methods=["POST"])
def process_register():
	success = False
	select_query = "SELECT * FROM users WHERE username = :username OR email = :email"

	select_data = {
		"username": request.form["username"],
		"email": request.form["email"]
	}

	if len(mysql.query_db(select_query, select_data)) == 0: # Valid registration
		success = True

		insert_query = "INSERT INTO users (username, password_hash, password_salt, email, created_at, updated_at) "
		insert_query += "VALUES (:username, :password_hash, :password_salt, :email, :now, :now)"

		password_salt = str(binascii.b2a_hex(os.urandom(15)))

		insert_data = {
			"username": request.form["username"],
			"password_hash": md5.new(request.form["password"] + password_salt).hexdigest(),
			"password_salt": password_salt,
			"email": request.form["email"],
			"now": str(datetime.datetime.now()) # because NOW() doesn't work for some reason
		}

		mysql.query_db(insert_query, insert_data)

		setup_session()

		session["username"] = request.form["username"]

	return render_template("register.html", success=success)

@app.route("/logout")
def logout():
	session["username"] = None

	return render_template("index.html")

app.run(debug=True)