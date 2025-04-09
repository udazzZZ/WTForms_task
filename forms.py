from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm


class SignUpForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("email", validators=[DataRequired(), Length(min=6, max=50)])
    age = IntegerField("age", validators=[DataRequired()])

    submit = SubmitField("Sign Up")

    @staticmethod
    def validate_email(form, field):
        if "@" not in field.data:
            raise ValidationError("Invalid email address")
        if "." not in field.data.split("@")[1]:
            raise ValidationError("Invalid email address")

    @staticmethod
    def validate_name(form, field):
        for char in field.data:
            if char in "0123456789":
                raise ValidationError("Name should not contain numbers")

    @staticmethod
    def validate_age(form, field):
        if field.data < 0:
            raise ValidationError("Age should be a positive number")
        elif field.data not in range(1, 120):
            raise ValidationError("Age should be between 1 and 120")


class UpdateForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("email", validators=[DataRequired(), Length(min=6, max=50)])
    age = IntegerField("age", validators=[DataRequired()])

    submit = SubmitField("Update")

    @staticmethod
    def validate_email(form, field):
        if "@" not in field.data:
            raise ValidationError("Invalid email address")
        if "." not in field.data.split("@")[1]:
            raise ValidationError("Invalid email address")

    @staticmethod
    def validate_name(form, field):
        for char in field.data:
            if char in "0123456789":
                raise ValidationError("Name should not contain numbers")

    @staticmethod
    def validate_age(form, field):
        if field.data < 0:
            raise ValidationError("Age should be a positive number")
        elif field.data not in range(1, 120):
            raise ValidationError("Age should be between 1 and 120")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
