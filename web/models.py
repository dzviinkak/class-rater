#import packages

from sqlalchemy import create_engine, Column, Text, Integer, Date, Boolean, ForeignKey, Enum, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from web import login_manager
from web import db

# creating the tables for the database

# Define models
# Create and initialize User, Review_likes, Review, Course, Major, Professors, Concentration objects

# PROBLEM we do not have a way of figuring out whether the student actually took the class

# TODO double check the normalization
# TODO introduce constraints on possible values in some columns (example: reviews)

# normalization resource: https://docs.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# # User to inherit from MixIn to take advantage of
# # is_active(), is_authenticated(), is_anonymous()
class User(db.Model, UserMixin):
    """
        This class represents a User that can login into the system.
        The password is encrypted.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, index = True,unique=True,nullable=False)
    #first_name = Column(Text)
    #last_name = Column(Text)
    email = db.Column(db.String(120), index=True, unique=True)
    signup_date = db.Column(DateTime(), index=True, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User: (id={0}, username={1})".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   # return True or False

class Major(db.Model):
    """
        This class represents a Major with is, short_name, full_name as attributes.
    """
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key = True)
    short_name = db.Column(db.Text, index = True)
    full_name = db.Column(db.Text)
    
    def __repr__(self):
        return "<Major: (id={0}, short_name={1}, long_name={2})>".format(self.id, self.short_name, self.full_name)

class Concentration(db.Model):
    """
        This class represents Concentration with id, name and major_id as attributes.
    """
    __tablename__ = 'concentrations'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    major_id = db.Column(db.Integer, ForeignKey('majors.id'), index = True)

    def __repr__(self):
        return "<Concentration: (id={0}, name={1}, major={2})>".format(self.id, self.name, self.major_id)

class Course(db.Model):
    """
        This class represents Course with id, short_name, long_name as attributes.
    """
    __tablename__ = 'courses'
    id = db.Column(Integer, primary_key = True)
    #concentration_id = Column(Text, ForeignKey('concetrations.id'))
    short_name = db.Column(db.Text, index = True, unique = True)
    long_name = db.Column(db.Text, unique = True)
    # TODO introduce constraints
    # refers to core/concentration
    type = Column(Enum('core','concentration','cornerstone', 'tutorial', name='course_type'))

    def __repr__(self):
        return "<Course: (id={0}, code={1})".format(self.id, self.short_name)

# potentially add prerequisites table as well
# separate table because a course can be in several concentrations and vice versa
class Course_concentration(db.Model):
    """
        This class represents Courses and concentrations (many-to-many relationship).
        This table is separate from both Courses and Concentrations tables to adhere to rules of 
        normalization of databases. 
    """
    __tablename__ = 'course_concentration'
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, ForeignKey('courses.id'),index= True)
    concentration_id = db.Column(db.Integer, ForeignKey('concentrations.id'), index= True)


class Professor(db.Model):
    """
        This class represents a Professor with id, first name and last name as attributes.
    """
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    first_name = db.Column(db.Text, index = True)
    last_name = db.Column(db.Text, index = True)
    
    def __repr__(self):
        return "<Professor(id={0}, first_name={1}, last_name={2})".format(self.id, self.first_name, self.last_name)

class Review(db.Model):
    """
        This class represents a Review of a Course instance with a range of attributes.
    """
    # TODO ask Mihn if I need to normalize it a bit more
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    course_id = db.Column(db.Integer, ForeignKey('courses.id'), index = True)
    prof_id = db.Column(db.Integer, ForeignKey('professors.id')) # decide whether to add index in here
    # TODO introduce constraints on all the features below except for date
    text = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    quality = db.Column(db.Integer)
    workload = db.Column(db.Integer)
    date = db.Column(db.Date)
    
    
    def __repr__(self):
        return "<Review(id={0}, course_id={2})".format(self.id, self.course_id)

    
class Review_likes(db.Model):
    """
        This class represents which Users have (dis)liked a Review. It has a many-to-many relationship.
        Many Users might have (dis)liked a review. Many reviews might correspond to one User.
    """
    __tablename__ = 'review_likes'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable = False)
    review_id = db.Column(db.Integer, ForeignKey('reviews.id'), index = True, nullable = False)
    # set constraints, only 2 values are possible
    like = db.Column(db.Boolean, nullable = False)
    
    def __repr__(self):
        if self.like == 0:
            like = 'Like'
        else:
            like = 'Dislike'
        return "<Review and corresponding (dis)like (id={0}, user_id={1}, review_id={2}, like={3})>".format(self.id, self.user_id, self.review_id, like)

db.drop_all()
db.create_all()