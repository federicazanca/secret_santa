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
