import random
from faker import Faker
from . import College, Essay, Major, RecommendationLetter, TestScore
from .. import db
from sqlalchemy.orm import validates


student_colleges = db.Table('student_colleges',
                            db.Column('college_id', db.Integer,
                                      db.ForeignKey('college.id')),
                            db.Column('student_profile_id', db.Integer,
                                      db.ForeignKey('student_profile.id'))
                            )

student_majors = db.Table('student_majors',
                          db.Column('major_id', db.Integer,
                                    db.ForeignKey('major.id')),
                          db.Column('student_profile_id', db.Integer,
                                    db.ForeignKey('student_profile.id'))
                          )


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates="student_profile")
    # PERSONAL INFO
    high_school = db.Column(db.String, index=True)
    district = db.Column(db.String, index=True)
    city = db.Column(db.String, index=True)
    state = db.Column(db.String, index=True)
    graduation_year = db.Column(db.String, index=True)
    grade = db.Column(db.Integer, index=True)
    # ACADEMIC INFO
    gpa = db.Column(db.Float, index=True)
    test_scores = db.relationship(
        'TestScore', backref='student_profile', lazy=True)
    majors = db.relationship('Major', secondary=student_majors,
                             backref=db.backref('student_profiles', lazy='dynamic'))
    colleges = db.relationship('College', secondary=student_colleges,
                               backref=db.backref('student_profiles', lazy='dynamic'))
    # APPLICATION INFO
    # either 'Incomplete' or 'Complete'
    fafsa_status = db.Column(db.String, index=True, default='Incomplete')
    common_app_essay = db.Column(db.String, index=True, default='') # link to common app essay
    common_app_essay_status = db.Column(db.String, index=True, default='Incomplete')
    essays = db.relationship('Essay')
    recommendation_letters = db.relationship('RecommendationLetter')

    @validates('common_app_essay_status')
    def validate_status(self, key, status):
        assert status in ['Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done']
        return status

    @staticmethod
    def generate_fake():
        fake = Faker()
        year = random.choice([['2018', '12'], ['2019', '11'], ['2020', '10']])
        fafsa_status = random.choice(['Incomplete', 'Complete'])
        essay_status = random.choice(['Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done'])
        profile = StudentProfile(
            high_school='{} High School'.format(fake.street_name()),
            district='{} District'.format(fake.city()),
            city=fake.city(),
            state=fake.state(),
            graduation_year=year[0],
            grade=year[1],
            gpa=round(random.uniform(2, 4), 2),
            test_scores=TestScore.generate_fake(),
            majors=random.sample(Major.query.all(), 3),
            fafsa_status=fafsa_status,
            colleges=random.sample(College.query.all(), 3),
            common_app_essay='https://google.com',
            common_app_essay_status=essay_status,
            essays=Essay.generate_fake(),
            recommendation_letters=RecommendationLetter.generate_fake()
        )
        return profile

    def __repr__(self):
        s = '<Student Profile\n'
        s += 'High School: {}\n'.format(self.high_school)
        s += 'District: {}\n'.format(self.district)
        s += 'City, State: {}, {}\n'.format(self.city, self.state)
        s += 'Gradution Year: {}\n'.format(self.graduation_year)
        s += 'Grade: {}\n'.format(self.grade)
        s += 'GPA: {}\n'.format(self.gpa)
        s += 'Test Scores: {}\n'.format(self.test_scores)
        s += 'Majors: {}\n'.format(','.join([m.name for m in self.majors]))
        s += 'Colleges: {}\n'.format(','.join([c.name for c in self.colleges]))
        s += 'FAFSA Status {}\n'.format(self.fafsa_status)
        s += 'Common App Essay: {}\n'.format(self.common_app_essay)
        s += 'Essays: {}\n'.format(self.essays)
        s += 'Recommendation Letters: {}'.format(
            self.recommendation_letters) + '>'
        return s
