INSERT INTO user_account (first_name, last_name, username, user_password)
    VALUES
    ('hayden', 'kreuter', 'hayden7177', 'abc123')
;

INSERT INTO post (title, post_type, embedded_video_link, stored_video_path, stored_image_path, post_text, posted_by_id)
    VALUES
    ('First Post', 'text', null, null, null, 'Maecenas aliquam maecenas ligula nostra, accumsan taciti. Sociis mauris in integer, a dolor netus non dui aliquet, sagittis felis sodales, dolor sociis mauris, vel eu libero cras. Faucibus at. Arcu habitasse elementum est, ipsum purus pede porttitor class, ut adipiscing, aliquet sed auctor, imperdiet arcu per diam dapibus libero duis.', 1)
;

INSERT INTO post (title, post_type, embedded_video_link, stored_video_path, stored_image_path, post_text, posted_by_id)
    VALUES
    ('GOl!!!!', 'embedded_video', 'https://www.youtube.com/embed/ZkIGO2UA-u8', null, null, null, 1)
;

INSERT INTO user_comment (comment_text, parent_post_id, parent_comment_id, commented_by_id)
    VALUES
    ('This is cool', 1, null, 1)
;
INSERT INTO user_comment (comment_text, parent_post_id, parent_comment_id, commented_by_id)
    VALUES
    ('LOL', 2, null, 1)
;
INSERT INTO user_comment (comment_text, parent_post_id, parent_comment_id, commented_by_id)
    VALUES
    ('NICE', 2, null, 1)
;