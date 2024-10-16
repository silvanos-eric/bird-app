import os

from flask import Flask, jsonify, make_response
from flask.json.provider import DefaultJSONProvider
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import Bird, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DefaultJSONProvider.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)


api.add_resource(Birds, '/birds')


class BirdByID(Resource):

    def get(self, id):
        bird = db.session.get(Bird, id).to_dict()
        return bird


api.add_resource(BirdByID, '/birds/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
