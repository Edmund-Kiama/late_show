# models.py
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from config import db 

# Define the Episode model
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    serialize_rules = ('-appearances.episode', '-guests.episodes',)


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    air_date = db.Column(db.String)

    # Relationships
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes')

    
    

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "air_date": self.air_date
        }

# Define the Guest model
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    serialize_rules = ('-appearances.guest', '-episodes.guests',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String)

    # Relationships
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests')

    
    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }

# Define the Appearance model
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    serialize_rules = ('-episode.appearances', '-guest.appearances',)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    
    

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "episode_id": self.episode_id,
            "guest_id": self.guest_id,
            "episode": self.episode.to_dict(),
            "guest": self.guest.to_dict()
        }
