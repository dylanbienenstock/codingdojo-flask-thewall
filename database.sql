CREATE DATABASE IF NOT EXISTS walldb;

CREATE TABLE IF NOT EXISTS walldb.users (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(255) NULL,
	password_hash VARCHAR(255) NULL,
	password_salt VARCHAR(255) NULL,
	email VARCHAR(255) NULL,
	created_at DATETIME NULL,
	updated_at DATETIME NULL,
	PRIMARY KEY (id));
    
CREATE TABLE IF NOT EXISTS walldb.messages (
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NULL,
    message_text VARCHAR(255) NULL,
	created_at DATETIME NULL,
	updated_at DATETIME NULL,
	PRIMARY KEY (id));
    
CREATE TABLE IF NOT EXISTS walldb.comments (
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NULL,
    message_id INT NULL,
    comment_text VARCHAR(255) NULL,
	created_at DATETIME NULL,
	updated_at DATETIME NULL,
	PRIMARY KEY (id));