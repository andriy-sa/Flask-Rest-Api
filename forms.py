import os
import wtforms as form
from flask_wtf import Form
from wtforms import validators
from models.user import User
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from app import app
from helpers import str_random


class LoginForm(Form):
    email = form.StringField('email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])
    password = form.PasswordField('password', validators=[
        validators.DataRequired()
    ])
    remember = form.BooleanField('remember', default=False)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False
        else:
            return True


class CompanyForm(Form):
    name = form.StringField('name', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    address = form.StringField('address', validators=[
        validators.DataRequired(),
        validators.Length(max=255)
    ])
    logo = form.FileField('logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'])
    ])

    def upload_logo(self):
        f = self.logo.data
        filename = "%s%s" % (str_random(8), secure_filename(f.filename))
        f.save(os.path.join(
            app.config.get('STATIC_DIR'), 'uploads', filename
        ))
        return filename

    def remove_logo(self, logo):
        try:
            os.remove(os.path.join(
                app.config.get('STATIC_DIR'), 'uploads', logo
            ))
        except:
            pass


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
    company_id = form.SelectField('company_id', validators=[validators.DataRequired(), ])

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
    company_id = form.SelectField('company_id', validators=[validators.DataRequired(), ])

    def set_user_id(self, user_id):
        self.user_id = user_id

    def validate_email(self, field):
        user = User.where('email', field.data).where('id', '!=', self.user_id).first()
        if user:
            raise form.ValidationError(message='User with this email already exist')
