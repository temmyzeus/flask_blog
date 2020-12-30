from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """A Form Object for Registration."""

    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])

    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=8)])

    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                                 Length(min=8),
                                                 EqualTo("password")])

    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """A Form Object for Login."""

    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=8)])

    # Add Remember Me to make user stay active after some while
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")
