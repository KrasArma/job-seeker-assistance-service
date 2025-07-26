
"""
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    link VARCHAR NOT NULL,
    salary VARCHAR,
    company VARCHAR,
    position VARCHAR,
    responded BOOLEAN DEFAULT TRUE,
    resume_id INTEGER REFERENCES resumes(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR DEFAULT 'applied',
    basket VARCHAR,
    rate INTEGER,
    score_match FLOAT,
    score_best FLOAT,
    contact1 VARCHAR,
    contact2 VARCHAR,
    comment VARCHAR
);
"""
