from app import db
from datetime import datetime
from sqlalchemy import and_, or_, not_

class Directions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_key = db.Column(db.String(16), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Directions {} || {} || {}>'.format(self.id, self.voter_key, self.timestamp)    


class FPTPVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_key = db.Column(db.String(16), index=True, unique=False)
    candid = db.Column(db.String(40), index=True, unique=False)
    riding = db.Column(db.String(50), index=True, unique=False)
    timestamp = db.Column(db.String(10), index=True, unique=False)
    election = db.Column(db.String(30), index=True, unique=False)
    
    def __repr__(self):
        return '<FPTPVote {} || {} || {} || {} || {}>'.format(self.voter_key, self.candid, self.riding, self.timestamp, self.election)    


class MMPVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_key = db.Column(db.String(16), index=True, unique=False)
    candid = db.Column(db.String(40), index=True, unique=False)
    riding = db.Column(db.String(50), index=True, unique=False)
    timestamp = db.Column(db.String(10), index=True, unique=False)
    party = db.Column(db.String(20), index=True, unique=False)
    election = db.Column(db.String(30), index=True, unique=False)

    def __repr__(self):
        return '<MMPVote {} || {} || {} || {} || {} || {}>'.format(self.voter_key, self.candid, self.riding, self.timestamp, self.party, self.election)    


class lprvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_key = db.Column(db.String(16), index=True, unique=False)
    rank = db.relationship('LPRRank', backref='ballot', lazy='dynamic')
    riding = db.Column(db.String(50), index=True, unique=False)
    timestamp = db.Column(db.String(10), index=True, unique=False)
    district = db.Column(db.String(50), index=True, unique=False) 
    election = db.Column(db.String(30), index=True, unique=False)

    def __repr__(self):
#        return (self.voter_key, self.riding, self.timestamp, self.district, #self.election)
        return '<lprvote {} || {} || {} || {} || {}>'.format(self.voter_key, self.riding, self.timestamp, self.district, self.election)    


class LPRRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candid = db.Column(db.String(40), index=True, unique=False)
    rank = db.Column(db.Integer, index=True, unique=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('lprvote.id'))

    def __init__(self):
        return (candid, rank, user_id)

    def __repr__(self):
#        return (self.candid, self.rank, self.user_id)
        return '<LPRRank {} || {} || {}>'.format(self.candid, self.rank, self.user_id) 
