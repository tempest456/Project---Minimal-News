from flask_wtf import FlaskForm
from wtforms import (BooleanField, RadioField, SelectMultipleField,
                     StringField, SubmitField, ValidationError, widgets)
from wtforms.validators import DataRequired, Email

from ..models import User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Email(message='Must be an email!')])
    preferred_time = RadioField('Preferred time', choices=[(
        'morning', 'Morning'), ('noon', 'Noon'), ('evening', 'Evening')],
        validators=[DataRequired(message='Cannot be empty!')])
    categories = MultiCheckboxField('Categories', choices=[
        ('nepal', 'Nepal'),
        ('world', 'World'),
        ('business', 'Finance'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('science-technology', 'Technology'),
    ])
    corona_update = BooleanField('Corona Update')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')
