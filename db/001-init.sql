CREATE TABLE admins (
    id SERIAL PRIMARY KEY, 
    nome TEXT, 
    "password" TEXT
);

INSERT INTO admins (
    nome,
    "password"
) VALUES ('fedi', '1234'), ('bigol', 'big');

CREATE TABLE elenco (
    id SERIAL PRIMARY KEY,
    nome TEXT 
);

CREATE TABLE persone (
    id SERIAL PRIMARY KEY, 
    lista_id SERIAL REFERENCES elenco(id), 
    nome TEXT, 
    email TEXT
);
