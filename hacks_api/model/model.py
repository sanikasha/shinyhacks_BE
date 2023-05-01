from sqlalchemy import Column, Integer, String, Text
from .. import db
from sqlalchemy.exc import IntegrityError
import json
from werkzeug.security import generate_password_hash, check_password_hash

# 
# Leaderboard DB class that maps leaderboard SQL table 
#
class Student(db.Model):
    __tablename__ = "student"

    # 
    # Leaderboard DB columns for easy, medium and hard points with user info
    #    
    id = Column(Integer, primary_key=True)
    _name = Column(String(255), unique=True, nullable=False)
    _GPA = Column(Integer, nullable=False)
    _grade = Column(Integer, nullable=False)

    # 
    # Leaderboard DB class constructor 
    #
    def __init__(self, name, GPA, grade):
        self._name = name
        self._GPA = GPA
        self._grade = grade

    # 
    # Leaderboard DB class string representation of an object
    #
    def __repr__(self):
        return "<Student(id='%s', name='%s', GPA='%s', grade='%s'>" % (
            self.id,
            self.name,
            self.GPA,
            self.grade,
        )

    # 
    # Returns Leaderboard username
    #    
    @property
    def name(self):
        return self._name

    # 
    # Sets Leaderboard username
    #        
    @name.setter
    def name(self, value):
        self._name = value

    # 
    # checks Leaderboard username valid
    #            
    def is_name(self, name):
        return self._name == name

    # 
    # Returns Leaderboard easy points
    #        
    @property
    def GPA(self):
        return self._GPA

    # 
    # Sets Leaderboard easy points
    #        
    @GPA.setter
    def GPA(self, value):
        self._GPA = value

    # 
    # Sets Leaderboard medium points
    #            
    @property
    def grade(self):
        return self._grade

    # 
    # Sets Leaderboard medium points
    #        
    @grade.setter
    def grade(self, value):
        self._grade = value

  

    # 
    # Converts Leaderboard to dictionary
    #            
    def to_dict(self):
        return {"id": self.id, "name": self.name, "GPA": self.GPA, "grade": self._grade}

    # 
    # Converts Leaderboard to string values
    #                
    def __str__(self):
        return json.dumps(self.read())

    # 
    # Creates Leaderboard database
    #                
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
    # 
    # Returns Leaderboard name value pairs
    #            
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "GPA": self.GPA,
            "grade": self.grade,
        }

    # 
    # Updates Leaderboard DB rows for points and user data
    #                
    def update(self, name="", GPA="", grade=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(GPA) > 0:
            self.GPA = GPA
        if len(grade) > 0:
            self.grade = grade
        db.session.add(self)
        db.session.commit()
        return self

    # 
    # Delets Leaderboard row from teh DB
    #                
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # 
    # Initializes Leaderboard DB with test data
    #            
def init_students():
    """Create database and tables"""
    # db.create_all()
    """Tester data for table"""
    s1 = Student(name="sanika", GPA=4,
                     grade=12)
    s2 = Student(name="kaylee", GPA=4,
                     grade=12)
    s3 = Student(name="jiya", GPA=4,
                     grade=12)
    s4 = Student(name="trent", GPA=4,
                     grade=12)
    students = [s1, s2, s3, s4]

    """Builds sample user/note(s) data"""
    for s in students:
        try:
            '''add user to table'''
            object = s.create()
            print(f"Created new uid {object.name}")
            db.session.add(s)
            db.session.commit()
        except:
            '''fails with bad or duplicate data'''
            print(f"Records exist uid {s.name}, or error.")
