CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    grade TEXT,
    location TEXT,
    user_id INTEGER REFERENCES users,
    time TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    route_id INTEGER REFERENCES routes,
    time TIMESTAMP
);