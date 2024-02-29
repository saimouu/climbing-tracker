CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
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
    time TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE flashes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users, 
    route_id INTEGER REFERENCES routes, 
    flash BOOLEAN
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY, 
    city TEXT, 
    country TEXT,
    name TEXT
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    img BYTEA,
    name TEXT,
    mimetype TEXT,
    route_id INTEGER REFERENCES routes
);

-- Test locations
INSERT INTO locations (city, country, name) VALUES ('Espoo', 'Finland', 'Boulderkeskus Espoo');
INSERT INTO locations (city, country, name) VALUES ('Helsinki', 'Finland', 'Boulderkeskus Herttoniemi');
INSERT INTO locations (city, country, name) VALUES ('Oulu', 'Finland', 'Oulun kiipeilykeskus');
