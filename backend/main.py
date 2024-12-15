from typing import Union
from pathlib import Path
import psycopg2
from fastapi import FastAPI, HTTPException
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

params = {
        "host": "postgres",
        "port": "5432",
        "dbname": "santa",
        "user": "admin",
        "password": "password"
    }


class User(BaseModel):
    nome:str
    password:str

@santapp.post("/login")
def login(user:User):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id FROM admins WHERE nome = %s and \"password\"= %s;", (user.nome, user.password))
                    result = cur.fetchone()
                    token = f"token_{result[0]}"
                    return token
                except (Exception, psycopg2.DatabaseError):
                    raise HTTPException(status_code=401, detail="Invalid credentials")



class Persona(BaseModel):
    nome:str
    email:str


@santapp.get("/extract")
def extract_random_name():
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT NOME FROM elenco ORDER BY RANDOM() LIMIT 1")
            result = cur.fetchone()
    
    return {"random_name": result[0]}


class Lista(BaseModel):
    titolo:str  


@santapp.post("/lista")
def make_list(lista:Lista):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("Insert INTO elenco (nome) VALUES (%s) ;", (lista.titolo,))
            conn.commit()
            cur.execute("SELECT id FROM elenco WHERE nome = %s;", (lista.titolo,))
            id = cur.fetchone()[0]
            
    return {"id":id}


@santapp.post("/lista/{id}")
def add_persona(persona:Persona, id):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM elenco WHERE id = %s;", (id,))
            cur.execute("INSERT INTO persone (lista_id, nome, email) VALUES (%s, %s, %s);", (id, persona.nome, persona.email,))
            conn.commit()


@santapp.get("/lista")
def show_list():
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome FROM elenco")
            result = cur.fetchall()
    
    return [{"id": l[0], "titolo": l[1]} for l in result]


@santapp.get("/lista/{id}")
def show_persone(id):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nome, email FROM persone WHERE lista_id = %s;", (id,))
            persone = cur.fetchall()
    
    return [{"nome": l[0], "email": l[1]} for l in persone]
