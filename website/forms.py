from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, SelectMultipleField, PasswordField, BooleanField, DecimalField, DateField
from wtforms.validators import DataRequired, Email

class CreateProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    experience_level = SelectField('Experience Level', choices=[('', 'Select an Experience Level'), ('1', 'Beginner'), ('2', 'Intermediate'), ('3', 'Advanced')], validators=[DataRequired()])
    skills = SelectMultipleField('Skills', validators=[DataRequired()])
    submit = SubmitField('Create Project')

class CreateFileForm(FlaskForm):
    file_name = StringField('File Name', validators=[DataRequired()])
    file_path = StringField('File Path', validators=[DataRequired()])
    submit = SubmitField('Create File')

class CreateUserForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password*', validators=[DataRequired()])
    password2 = PasswordField('Password (Confirm)*', validators=[DataRequired()])
    age = DecimalField('Age', places=0, validators=[])
    experience = SelectField('Experience Level*', choices=[('', 'Select an Experience Level'), ('1', 'Beginner'), ('2', 'Intermediate'), ('3', 'Advanced')], validators=[DataRequired()])
    affiliation = StringField('Affiliation', validators=[])
    # interest = SelectMultipleField('Interest* (Hold CTRL to Select Multiple)', choices=[('1', 'Beginner'), ('2', 'Intermediate'), ('3', 'Advanced')], validators=[DataRequired()])
    interest = SelectMultipleField('Interest* (Hold CTRL to Select Multiple)', validators=[DataRequired()])
    #work_time = DateField('Start Date', validators=[DataRequired()])
    submit = SubmitField('Create User')
