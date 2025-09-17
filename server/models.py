from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Association table to store many-to-many relationship between sessions and speakers
session_speakers = db.Table(
    'session_speakers',
    db.metadata,
    db.Column('session_id', db.Integer, db.ForeignKey(
        'sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey(
        'speakers.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)


# Relationship mapping the event to related sessions
    sessions = db.relationship(
        'Session', backref='event', cascade='all, delete-orphan')
    
    speakers = association_proxy('sessions', 'speakers')
    
    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    speakers = db.relationship(
        'Speaker', secondary=session_speakers, backref='sessions')

    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    bio = db.relationship('Bio', backref='speaker', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'
