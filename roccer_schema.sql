DROP TABLE IF EXISTS user_account;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user_comment;
DROP TABLE IF EXISTS post_vote;
DROP TABLE IF EXISTS comment_vote;


CREATE TABLE IF NOT EXISTS user_account (
	user_account_id SERIAL NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	username VARCHAR(255) NOT NULL,
	user_password VARCHAR(255) NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id),
	UNIQUE (username)
);

DROP TYPE IF EXISTS post_t;
CREATE TYPE post_t AS ENUM('text', 'embedded_video', 'stored_video', 'stored_image');

CREATE TABLE IF NOT EXISTS post (
	post_id SERIAL NOT NULL,
	title VARCHAR(255) NOT NULL,
	post_type post_t NOT NULL,
	embedded_video_link VARCHAR(255) NULL,
	stored_video_path VARCHAR(255) NULL,
	stored_image_path VARCHAR(255) NULL,
	post_text VARCHAR(255) NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	posted_by_id INT NOT NULL,

	PRIMARY KEY (post_id),
	FOREIGN KEY (posted_by_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_comment (
	comment_id SERIAL NOT NULL,
	comment_text VARCHAR(255) NOT NULL, 
	created_at timestamptz NOT NULL DEFAULT now(),
	owner_post_id INT NOT NULL,
	owner_comment_id INT NULL,
	commented_by_id INT NOT NULL,
	
	PRIMARY KEY (comment_id),
	FOREIGN KEY (owner_post_id) REFERENCES post(post_id) ON DELETE CASCADE,
	FOREIGN KEY (owner_comment_id) REFERENCES user_comment(comment_id),
	FOREIGN KEY (commented_by_id) REFERENCES user_account(user_account_id)
);

CREATE TABLE IF NOT EXISTS post_vote (
	user_account_id INT NOT NULL,
	post_id INT NOT NULL, 
	upvote BOOLEAN NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id, post_id),
	FOREIGN KEY (user_account_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE,
	FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comment_vote (
	user_account_id INT NOT NULL,
	user_comment_id INT NOT NULL, 
	upvote BOOLEAN NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	PRIMARY KEY (user_account_id, user_comment_id),
	FOREIGN KEY (user_account_id) REFERENCES user_account(user_account_id) ON DELETE CASCADE,
	FOREIGN KEY (user_comment_id) REFERENCES user_comment(comment_id) ON DELETE CASCADE
);