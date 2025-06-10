from app import db
from flask_login import UserMixin
from sqlalchemy import Enum
from sqlalchemy.sql import func  # for default timestamps
from datetime import datetime,  timezone

# print("working)")
# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # auto-increment is implicit
#     name = db.Column(db.String(150), nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(256), nullable=False)  # hashed and stored
#     is_admin = db.Column(db.Boolean, default=False)

#     # For fee receipt verification
#     receipt_filename = db.Column(db.String(200))
#     receipt_status = db.Column(db.String(50), default='Not Submitted')  # Not Submitted, Pending, Verified, Rejected
#     receipt_uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

#     student = db.relationship('Student', back_populates='user', uselist=False)

# class Student(db.Model):
#     __tablename__ = 'Student'
#     student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     branch = db.Column(db.String(50))
#     gender = db.Column(Enum('Male', 'Female', 'Other'), nullable=True)
#     category = db.Column(Enum('General', 'DASA', 'EWS', 'OBC'), nullable=True)
#     fee_paid = db.Column(db.Boolean, default=False)
#     academic_year = db.Column(db.Integer, default=1)
#     program = db.Column(Enum('Btech', 'Mtech', 'PHD'), default='Btech')
#     allotments = db.relationship('Allotment', back_populates='student')
#     user = db.relationship('User', back_populates='student')
#     # double relationship creates a problem
#     # user = db.relationship('User', backref=db.backref('student', uselist=False))





# class Hostel(db.Model):
#     __tablename__ = 'Hostel'
#     hostel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(100), nullable=False)
#     category = db.Column(Enum('DASA', 'NON-DASA'), default='NON-DASA')
#     gender = db.Column(Enum('Male', 'Female', 'Other'), nullable=False)
#     year = db.Column(db.Integer, nullable=True)
#     program = db.Column(Enum('Btech', 'Mtech', 'PHD', 'MULTIPLE'), nullable=True)

#     rooms = db.relationship('Room', back_populates='hostel')


# class Room(db.Model):
#     __tablename__ = 'Room'
#     room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     hostel_id = db.Column(db.Integer, db.ForeignKey('Hostel.hostel_id'), nullable=False)
#     room_number = db.Column(db.String(10), nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     floor = db.Column(db.Integer, nullable=True)

#     hostel = db.relationship('Hostel', back_populates='rooms')
#     allotments = db.relationship('Allotment', back_populates='room')


# class Allotment(db.Model):
#     __tablename__ = 'Allotment'
#     allotment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'), nullable=False)
#     room_id = db.Column(db.Integer, db.ForeignKey('Room.room_id'), nullable=False)
#     allotment_date = db.Column(db.DateTime, default=func.now())

#     student = db.relationship('Student', back_populates='allotments')
#     room = db.relationship('Room', back_populates='allotments')

# print("no issues")


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # hashed password
    is_admin = db.Column(db.Boolean, default=False)

    receipt_filename = db.Column(db.String(200))
    receipt_status = db.Column(db.String(50), default='Not Submitted')  # Not Submitted, Pending, Verified, Rejected
    receipt_uploaded_at = db.Column(db.DateTime, default=func.now())  # use func.now() for current timestamp

    student = db.relationship('Student', back_populates='user', uselist=False)


class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50))

    gender = db.Column(Enum('Male', 'Female', 'Other', name='gender_enum'), nullable=True)
    category = db.Column(Enum('General', 'DASA', 'EWS', 'OBC', name='category_enum'), nullable=True)

    fee_paid = db.Column(db.Boolean, default=False)
    academic_year = db.Column(db.Integer, default=1)

    program = db.Column(Enum('Btech', 'Mtech', 'PHD', name='program_enum'), default='Btech')

    allotments = db.relationship('Allotment', back_populates='student')
    user = db.relationship('User', back_populates='student')


class Hostel(db.Model):
    __tablename__ = 'hostel'
    hostel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    category = db.Column(Enum('DASA', 'NON-DASA', name='hostel_category_enum'), default='NON-DASA')
    gender = db.Column(Enum('Male', 'Female', 'Other', name='hostel_gender_enum'), nullable=False)

    year = db.Column(db.Integer, nullable=True)
    program = db.Column(Enum('Btech', 'Mtech', 'PHD', 'MULTIPLE', name='hostel_program_enum'), nullable=True)

    rooms = db.relationship('Room', back_populates='hostel')


class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.hostel_id'), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=True)

    hostel = db.relationship('Hostel', back_populates='rooms')
    allotments = db.relationship('Allotment', back_populates='room')


class Allotment(db.Model):
    __tablename__ = 'allotment'
    allotment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=False)
    allotment_date = db.Column(db.DateTime, default=func.now())

    student = db.relationship('Student', back_populates='allotments')
    room = db.relationship('Room', back_populates='allotments')


# print("Models loaded without issues.")