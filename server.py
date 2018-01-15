from flask import Flask, render_template, request, session
from mysqlconnection import MySQLConnector
import os, md5, binascii

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

		insert_query = "INSERT INTO users (username, password_hash, password_salt, email, created at, updated_at) "
		insert_query += "VALUES (:username, :password_hash, :password_salt, :email, NOW(), NOW())"

		password_salt = binascii.b2a_hex(os.urandom(15))

		insert_data = {
			"username": request.form["username"],
			"password_hash": md5.new(request.form["password"] + password_salt).hexdigest(),
			"password_salt": password_salt,
			"email": request.form["email"]
		}

		mysql.query_db(insert_query, insert_data)

		setup_session()

		session["username"] = request.form["username"]

	return render_template("login.html", success=success)

@app.route("/register")
def login():
	setup_session()

	return render_template("register.html")

@app.route("/logout")
def logout():
	session["username"] = None

	return render_template("index.html")

app.run(debug=True)