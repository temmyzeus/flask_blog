from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User
from flask_login import current_user
from flask_blog import config


class RegistrationForm(FlaskForm):
    """A Form Object for Registration."""

    username = StringField(
        "Username",
        validators=[DataRequired(),
                    Length(min=2, max=20)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(),
                    Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(),
                    Length(min=8)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(),
                    Length(min=8),
                    EqualTo("password")]
    )

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username Taken. Please choose a different one!!")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email Taken!!. Please Choose Another!!")


class LoginForm(FlaskForm):
    """A Form Object for Login."""

    email = StringField(
        "Email",
        validators=[DataRequired(),
                    Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(),
                    Length(min=8)]
    )

    # Add Remember Me to make user stay active after some while
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """A form for Profile Details."""

    # Field to Collect Username
    username = StringField(
        "Username",
        validators=[DataRequired(),
                    Length(min=2, max=20)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(),
                    Email()]
    )

    picture = FileField(
        "Update Profile Picture",
        validators=[FileAllowed(config.allowed_image_extensions)]
    )

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                "Username Taken. Please choose a different one!!")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email Taken!!. Please Choose Another!!")
