# Docker_Python_Flask

## Build 
docker-compose build

## Run
docker-compose up

## Help 

https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-de


## Init DB
Nur bei anpassung der Datenbank-Models ausführen
Nach dem starten im Docker das Terminal öffnen und die folgenden Befehle ausführen. 

flask db init // Nur ausführen, falls noch keine Migration vorhanden. 
flask db migrate -m "Mein Kommentar zur anpassung "
flask db upgrade

## CMD API
curl -X POST -H "Authorization: sutermichael@bluewin.ch:1234" -H "Content-Type: application/json" -d '{"title": "Mein Beitrag", "content": "Inhalt des Beitrags"}' http://localhost:5000/api/posts

