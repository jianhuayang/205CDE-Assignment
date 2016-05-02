DROP TABLE IF EXISTS contact;


CREATE TABLE contact (
    id integer PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    message text NOT NULL
    );