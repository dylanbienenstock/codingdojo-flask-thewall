from flask import Flask, render_template, request, session, redirect
from mysqlconnection import MySQLConnector
import os, md5, binascii, datetime

app = Flask(__name__)
app.secret_key = ":)"
mysql = MySQLConnector(app, "walldb")

def setup_session():
	if not "username" in session:
		session["username"] = None

	if not "password_hash" in session:
		session["password_hash"] = None

@app.route("/")
def index():
	setup_session()
	messages = mysql.query_db("SELECT * FROM messages ORDER BY id DESC")

	return render_template("index.html", messages=messages)

################## LOG IN ##################

@app.route("/login")
def login():
	setup_session()

	if session["username"] == None:
		return render_template("login.html")

	return render_template("message.html", message="You are already logged in.")

@app.route("/login/process", methods=["POST"])
def process_login():
	select_query = "SELECT * FROM users WHERE username = :username"
	select_data = { "username": request.form["username"] }

	row_data = mysql.query_db(select_query, select_data)

	if len(row_data) > 0:
		password_hash = md5.new(request.form["password"] + row_data[0]["password_salt"]).hexdigest()

		if password_hash == row_data[0]["password_hash"]: # Successful login
			success = True

			setup_session()

			session["username"] = request.form["username"]
			session["password_hash"] = password_hash

			return redirect("/login/success")

	return render_template("login.html", message="Invalid log-in details.")

@app.route("/login/success")
def successful_login():
	return render_template("message.html", message="Successfully logged in.")

################## REGISTRATION ##################

@app.route("/register")
def register():
	if session["username"] == None:
		return render_template("register.html")

	return render_template("message.html", message="You are already logged in.")

@app.route("/register/process", methods=["POST"])
def process_register():
	select_query = "SELECT * FROM users WHERE username = :username OR email = :email"

	select_data = {
		"username": request.form["username"],
		"email": request.form["email"]
	}

	if len(mysql.query_db(select_query, select_data)) == 0: # Valid registration
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
		session["password_hash"] = insert_data["password_hash"]

		return redirect("/register/success")

	return render_template("register.html", message="Account with username or email already exists.")

@app.route("/register/success")
def successful_register():
	return render_template("message.html", message="Successfully registered.")

@app.route("/logout")
def logout():
	session["username"] = None

	return render_template("index.html")

app.run(debug=True)