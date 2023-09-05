from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from werkzeug.security import check_password_hash
from models import User, PostModel
from db import db

apiAuth = Blueprint("apiAuth", __name__)
api = Api(apiAuth)

# Definieren Sie ein Parser-Objekt, um die JSON-Anforderung zu analysieren
parser = reqparse.RequestParser()
parser.add_argument('inputTitle', type=str, required=True)
parser.add_argument('inputPost', type=str, required=True)

# JSON-Ausgabeformat für die Antwort definieren
post_fields = {
    'id': fields.Integer,
    'inputTitle': fields.String,
    'inputPost': fields.String,
    # Weitere Felder hinzufügen, falls erforderlich
}

# Erstellen Sie eine benutzerdefinierte Ressource für den API-Endpunkt
class CreatePostAPI(Resource):
    @marshal_with(post_fields)  # JSON-Formatierung für die Antwort aktivieren
    def post(self):
        # Benutzername und Passwort aus dem Header lesen
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return {'message': 'Authorization header is missing'}, 401

        # Extrahieren Sie Benutzername und Passwort aus dem Header
        try:
            username, password = auth_header.split(':')
        except ValueError:
            return {'message': 'Invalid Authorization header format'}, 401
   
        # Überprüfen Sie die Anmeldeinformationen in der Datenbank
        user = User.query.filter_by(email=username).first()
        if user is None or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401

        # Die Anmeldeinformationen sind korrekt, den JSON-Body parsen und speichern
        args = parser.parse_args()
        new_post = PostModel(
            inputTitle=args['inputTitle'],
            inputPost=args['inputPost']
        )

        db.session.add(new_post)
        db.session.commit()

        return new_post, 201  # Erfolgreiche Erstellung mit HTTP-Statuscode 201 erstellt



    @marshal_with(post_fields)  # JSON-Formatierung für die Antwort aktivieren
    def get(self, post_id=None):
                # Benutzername und Passwort aus dem Header lesen
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return {'message': 'Authorization header is missing'}, 401

        # Extrahieren Sie Benutzername und Passwort aus dem Header
        try:
            username, password = auth_header.split(':')
        except ValueError:
            return {'message': 'Invalid Authorization header format'}, 401

        # Überprüfen Sie die Anmeldeinformationen in der Datenbank
        user = User.query.filter_by(email=username).first()
        if user is None or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401

        if post_id is None:
            # Wenn keine post_id angegeben ist, alle Beiträge abrufen
            posts = PostModel.query.all()
            return posts
        else:
            # Wenn eine post_id angegeben ist, den einzelnen Beitrag abrufen
            post = PostModel.query.get(post_id)
            if post:
                return post
            else:
                return {'message': 'Post not found'}, 404

    def delete(self, post_id):
        # Benutzername und Passwort aus dem Header lesen
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return {'message': 'Authorization header is missing'}, 401

        # Extrahieren Sie Benutzername und Passwort aus dem Header
        try:
            username, password = auth_header.split(':')
        except ValueError:
            return {'message': 'Invalid Authorization header format'}, 401

        # Überprüfen Sie die Anmeldeinformationen in der Datenbank
        user = User.query.filter_by(email=username).first()
        if user is None or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401

        # Den Beitrag löschen, falls vorhanden
        post = PostModel.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return {'message': 'Post deleted successfully'}
        else:
            return {'message': 'Post not found'}, 404

# Fügen Sie die API-Endpunkte zur Anwendung hinzu
# Fügen Sie den API-Endpunkt zur Anwendung hinzu
api.add_resource(CreatePostAPI, '/api/posts','/api/posts/<int:post_id>')


