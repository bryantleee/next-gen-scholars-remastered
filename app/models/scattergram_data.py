import random
from faker import Faker
from sqlalchemy.orm import validates
from .. import db


class ScattergramData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=True)
    college = db.Column(db.String, index=True)
    ed_status = db.Column(db.String, index=True)
    GPA = db.Column(db.Float, index=True)
    SAT2400 = db.Column(db.Integer, index=True, nullable=True)
    SAT1600 = db.Column(db.Integer, index=True, nullable=True)
    ACT = db.Column(db.Integer, index=True, nullable=True)
    fin_aid_perc = db.Column(db.Integer, index=True, nullable=True)
    high_school = db.Column(db.String, index=True, nullable=True)

    def __repr__(self):
        return '<ScattergramData {},{},{},{},{},{},{},{},{}>'.format(self.name, self.college, self.ed_status,
                                                                 self.GPA, self.SAT2400, self.SAT1600,
                                                                 self.ACT, self.fin_aid_perc, self.high_school)
