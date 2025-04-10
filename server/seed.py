from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    print("Clearing old data...")
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    print("Seeding episodes...")
    # Updated to use correct field names 'title' and 'air_date'
    ep1 = Episode(title="Episode 1", air_date="1/11/99")
    ep2 = Episode(title="Episode 2", air_date="1/12/99")
    ep3 = Episode(title="Episode 3", air_date="1/13/99")

    db.session.add_all([ep1, ep2, ep3])
    db.session.commit()

    print("Seeding guests...")
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")

    db.session.add_all([g1, g2, g3])
    db.session.commit()

    print("Seeding appearances...")
    # Need to add the episodes and guests first to make sure they are assigned IDs
    a1 = Appearance(rating=4, episode_id=ep1.id, guest_id=g1.id)
    a2 = Appearance(rating=5, episode_id=ep2.id, guest_id=g3.id)
    a3 = Appearance(rating=3, episode_id=ep3.id, guest_id=g2.id)

    db.session.add_all([a1, a2, a3])
    db.session.commit()

    print("Done seeding!")