from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

# Login form for user authentication
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Registration form for new users
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    # Hidden fields for favorite team and driver (selected via JS)
    favorite_team = HiddenField()
    favorite_driver = HiddenField()
    submit = SubmitField('Register')
    
# Edit profile form for updating user info
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    favorite_team = SelectField('Favorite Team', choices=[], validators=[DataRequired()])
    favorite_driver = SelectField('Favorite Driver', choices=[], validators=[DataRequired()])
    bio = TextAreaField('Bio')
    profile_pic = FileField('Profile Picture')
    submit = SubmitField('Save Changes')
    
# Forgot password form for requesting password reset
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

# Prediction upload form for submitting race predictions
class UploadPredictionForm(FlaskForm):
    predicted_winner = SelectField('Predicted Race Winner', choices=[], validators=[DataRequired()])
    fastest_lap = SelectField('Fastest Lap Driver', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit Prediction')