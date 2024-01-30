CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    grade TEXT,
    location TEXT,
    user_id INTEGER REFERENCES users
);