from flask_wtf import Form
from wtforms import validators
import wtforms as form
from models.company import Company
from models.user import User


class CompanyForm(Form):
    name = form.StringField('name', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    address = form.StringField('address', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])


class UserForm(Form):
    username = form.StringField('username', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    email = form.StringField('email', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(max=255)
    ])
    first_name = form.StringField('first_name', validators=[
        validators.Length(max=255)
    ])
    last_name = form.StringField('last_name', validators=[
        validators.Length(max=255)
    ])
    country = form.StringField('country', validators=[
        validators.Length(max=255)
    ])
    city = form.StringField('city', validators=[
        validators.Length(max=255)
    ])
    phone = form.StringField('phone', validators=[
        validators.Length(max=255)
    ])
    password = form.PasswordField('password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=16)
    ])
    company_id = form.SelectField('company_id', validators=[validators.DataRequired(), ],
                                  choices=[(str(c.id), str(c.id)) for c in Company.select('id').get()])

    def validate_email(self, field):
        user = User.where('email', field.data).first()
        if user:
            raise form.ValidationError(message='User with this email already exist')


class UserUpdateForm(Form):
    username = form.StringField('username', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    email = form.StringField('email', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(max=255)
    ])
    first_name = form.StringField('first_name', validators=[
        validators.Length(max=255)
    ])
    last_name = form.StringField('last_name', validators=[
        validators.Length(max=255)
    ])
    country = form.StringField('country', validators=[
        validators.Length(max=255)
    ])
    city = form.StringField('city', validators=[
        validators.Length(max=255)
    ])
    phone = form.StringField('phone', validators=[
        validators.Length(max=255)
    ])
    company_id = form.SelectField('company_id', validators=[validators.DataRequired(), ],
                                  choices=[(str(c.id), str(c.id)) for c in Company.select('id').get()])

    def set_user_id(self, user_id):
        self.user_id = user_id

    def validate_email(self, field):
        user = User.where('email', field.data).where('id', '!=', self.user_id).first()
        if user:
            raise form.ValidationError(message='User with this email already exist')
