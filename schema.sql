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
    indoor BOOLEAN,
    visible BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    route_id INTEGER REFERENCES routes,
    time TIMESTAMP
);

CREATE TABLE flashes (
    user_id INTEGER REFERENCES users, 
    route_id INTEGER REFERENCES routes, 
    flash BOOLEAN
);