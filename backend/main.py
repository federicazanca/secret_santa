from typing import Union
from pathlib import Path
import psycopg2
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


santapp = FastAPI(middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
])

@santapp.get("/")
def read_root():
    return {"SECRET SANTA EXTRACTION"}

class Persona(BaseModel):
    nome:str
    email:str

# @santapp.put("/names")
# def add_persona(persona:Persona):
#     params={
#         "host":"postgres",
#         "port":"5432",
#         "dbname":"santa",
#         "user":"admin",
#         "password":"password"    
#     }

#     with psycopg2.connect(**params) as conn:
#         with conn.cursor() as cur:
#             cur.execute("INSERT INTO elenco (NOME) VALUES (%s)", (persona.nome,))
#             conn.commit()


@santapp.get("/extract")
def extract_random_name():
    params = {
        "host": "postgres",
        "port": "5432",
        "dbname": "santa",
        "user": "admin",
        "password": "password"
    }
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT NOME FROM elenco ORDER BY RANDOM() LIMIT 1")
            result = cur.fetchone()
    
    return {"random_name": result[0]}


class Lista(BaseModel):
    titolo:str  

@santapp.post("/lista")
def make_list(lista:Lista):
    params={
        "host":"postgres",
        "port":"5432",
        "dbname":"santa",
        "user":"admin",
        "password":"password"    
    }

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("Insert INTO elenco (nome) VALUES (%s) ;", (lista.titolo,))
            conn.commit()
            cur.execute("SELECT id FROM elenco WHERE nome = %s;", (lista.titolo,))
            id = cur.fetchone()[0]
            
    return {"id":id}

@santapp.post("/lista/:id")
def add_persona(persona:Persona, id):
    params={
        "host":"postgres",
        "port":"5432",
        "dbname":"santa",
        "user":"admin",
        "password":"password"    
    }

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("FROM elenco SELECT id WHERE id = %s;", (id,))
            cur.execute("CREATE TABLE IF NOT EXISTS persone (id SERIAL PRIMARY KEY, lista_id INT, nome TEXT, email TEXT)")
            cur.execute("INSERT INTO persone (lista_id, nome, email) VALUES %s %s;", (id, persona.nome, persona.email,))
            conn.commit()

@santapp.get("/lista")
def show_list():
    params = {
        "host": "postgres",
        "port": "5432",
        "dbname": "santa",
        "user": "admin",
        "password": "password"
    }
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome FROM elenco")
            result = cur.fetchall()
    
    return result

@santapp.get("/lista/{id}")
def show_persone():
    params = {
        "host": "postgres",
        "port": "5432",
        "dbname": "santa",
        "user": "admin",
        "password": "password"
    }
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nome, email FROM persone WHERE lista_id = %s;", (id,))
            persone = cur.fetchall()
    
    return persone