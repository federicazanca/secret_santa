# Backend

## POST /lista { titolo }
### -> { id }
Crea una nuova lista vuota e ritorna l'ID della lista

## POST /lista/:id { nome, email }
Aggiunge una nuova persona alla lista con :id

## GET /lista
### -> [ { id, titolo } ]
Ritorna l'elenco di tutte le lista con id e nome

## GET /lista/:id
### -> [ { nome, email } ]
Ritorna l'elenco di tutte le persone nella lista con nome e email
