# app.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import migrate, db
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize db and migrate here
migrate.init_app(app, db)
db.init_app(app)
api = Api(app)

# Import models AFTER db initialization
from models import Episode, Guest, Appearance

# ROUTES 
# REST api
class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        return [ep.to_dict() for ep in episodes], 200
    
api.add_resource(Episodes, '/episodes')

class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if episode:
            episode_dict = episode.to_dict()
            episode_dict["appearances"] = [
                {
                    "id": ap.id,
                    "rating": ap.rating,
                    "episode_id": ap.episode_id,
                    "guest_id": ap.guest_id,
                    "guest": ap.guest.to_dict()
                }
                for ap in episode.appearances
            ]
            return episode_dict, 200
        return {"error": "Episode not found"}, 404

api.add_resource(EpisodeByID, '/episodes/<int:id>')

class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        return [guest.to_dict() for guest in guests], 200
    
api.add_resource(Guests, '/guests')

class Appearances(Resource):
    def post(self):
        data = request.get_json()
        try:
            rating = data.get("rating")
            episode_id = data.get("episode_id")
            guest_id = data.get("guest_id")

            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")

            episode = Episode.query.get(episode_id)
            guest = Guest.query.get(guest_id)

            if not episode or not guest:
                raise ValueError("Invalid episode_id or guest_id.")

            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )
            db.session.add(new_appearance)
            db.session.commit()

            return new_appearance.to_dict(), 201

        except (ValueError, TypeError) as e:
            return {"errors": [str(e)]}, 400
        except IntegrityError:
            # used to undo uncommited changes.
            db.session.rollback()
            return {"errors": ["Database integrity error"]}, 400


api.add_resource(Appearances, '/appearances')

# ENTRY POINT 
if __name__ == '__main__':
    app.run(debug=True)

