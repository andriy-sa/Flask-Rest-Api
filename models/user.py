from orator import Model
from app import login_manager, bcrypt
from models import company
from orator.orm import belongs_to


class User(Model):
    __fillable__ = ['username', 'first_name', 'last_name', 'email', 'country', 'city', 'phone', 'password', 'is_admin', 'is_active']
    __hidden__ = ['password']

    @belongs_to('company_id', 'id')
    def company(self):
        return company.Company

    @staticmethod
    def make_password(password):
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return hash

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def authenticate(email, password):
        user = User.where('email', email).first()
        if user and user.check_password(password):
            return user
        return False

    @staticmethod

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True


@login_manager.user_loader
def _user_loader(user_id):
    return User.find(int(user_id))


def identity(payload):
    user_id = payload['identity']
    user = User.find(user_id)
    if user:
        return user.serialize()

    return None


def authenticate(email, password):
    user = User.where('email', email).first()
    if user and user.check_password(password):
        return user
    return False