from orator import Model
from app import login_manager, bcrypt
from models import company
from orator.orm import belongs_to


class User(Model):
    __fillable__ = ['username', 'first_name', 'last_name', 'email', 'country', 'city', 'phone', 'password', 'is_admin']
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
        user = User.query.filter(User.email == email).first()
        user = User.where('email', email).first()
        if user and user.check_password(password):
            return user
        return False


@login_manager.user_loader
def _user_loader(user_id):
    return User.find(int(user_id))
