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

@santapp.put("/names")
def add_persona(persona:Persona):
    params={
        "host":"postgres",
        "port":"5432",
        "dbname":"santa",
        "user":"admin",
        "password":"password"    
    }

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO elenco (NOME) VALUES (%s)", (persona.nome,))
            conn.commit()


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
            # Query per estrarre un nome casuale
            cur.execute("SELECT NOME FROM elenco ORDER BY RANDOM() LIMIT 1")
            result = cur.fetchone()
    
    return {"random_name": result[0]}


class Titolo(BaseModel):
    titolo:str  

@santapp.post("/lista")
def make_list(titolo:Titolo):
    params={
        "host":"postgres",
        "port":"5432",
        "dbname":"santa",
        "user":"admin",
        "password":"password"    
    }

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO elenco (NOME) VALUES (%s)", (persona.nome,))
            conn.commit()