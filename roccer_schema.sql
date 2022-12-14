DROP TABLE IF EXISTS comment_vote;
DROP TABLE IF EXISTS user_comment;
DROP TABLE IF EXISTS post_vote;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user_account;


CREATE TABLE IF NOT EXISTS user_account (
	user_account_id SERIAL NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	username VARCHAR(255) NOT NULL UNIQUE,
	user_password VARCHAR(255) NOT NULL,
	profile_path VARCHAR(255) NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id),
	UNIQUE (username)
);

DROP TYPE IF EXISTS post_t;
CREATE TYPE post_t AS ENUM('text', 'embedded_video', 'stored_video', 'stored_image');

CREATE TABLE IF NOT EXISTS post (
	post_id SERIAL NOT NULL,
	title VARCHAR(500) NOT NULL,
	post_type post_t NOT NULL,
	embedded_video_link VARCHAR(255) NULL,
	stored_video_path VARCHAR(255) NULL,
	stored_image_path VARCHAR(255) NULL,
	post_text VARCHAR(2000) NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	posted_by_id INT NULL,
	post_bot_stashed BOOLEAN NOT NULL DEFAULT false,

	PRIMARY KEY (post_id),
	FOREIGN KEY (posted_by_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_comment (
	comment_id SERIAL NOT NULL,
	comment_text VARCHAR(255) NOT NULL, 
	created_at timestamp NOT NULL DEFAULT now(),
	parent_post_id INT NOT NULL,
	parent_comment_id INT NULL,
	commented_by_id INT NOT NULL,
	
	PRIMARY KEY (comment_id),
	FOREIGN KEY (parent_post_id) REFERENCES post(post_id) ON DELETE CASCADE,
	FOREIGN KEY (parent_comment_id) REFERENCES user_comment(comment_id),
	FOREIGN KEY (commented_by_id) REFERENCES user_account(user_account_id)
);

CREATE TABLE IF NOT EXISTS post_vote (
	post_vote_id SERIAL NOT NULL,
	user_account_id INT NOT NULL,
	post_id INT NOT NULL, 
	upvote BOOLEAN NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id,post_vote_id),
	FOREIGN KEY (user_account_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE,
	FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment_vote (
	user_account_id INT NOT NULL,
	user_comment_id INT NOT NULL, 
	upvote BOOLEAN NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id, user_comment_id),
	FOREIGN KEY (user_account_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE,
	FOREIGN KEY (user_comment_id) REFERENCES user_comment(comment_id) ON DELETE CASCADE
);