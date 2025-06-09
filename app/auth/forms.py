from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')



class ReceiptUploadForm(FlaskForm):
    receipt = FileField('Upload Fee Receipt', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDFs only!')
    ])
    submit = SubmitField('Upload')


class StudentProfileForm(FlaskForm):
    branch = StringField('Branch', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    category = SelectField('Category', choices=[('General', 'General'), ('DASA', 'DASA'), ('EWS', 'EWS'), ('OBC', 'OBC')])
    academic_year = IntegerField('Academic Year', validators=[DataRequired()])
    program = SelectField('Program', choices=[('Btech', 'Btech'), ('Mtech', 'Mtech'), ('PHD', 'PHD')])
    submit = SubmitField('Submit Profile')

class Roomid(FlaskForm):
    roomid = SelectField("Choose Room", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")