from orator import Model
from models import user,project
from orator.orm import has_many


class Company(Model):
    __fillable__ = ['name', 'address', 'logo']

    @has_many('company_id', 'id')
    def users(self):
        return user.User

    @has_many('company_id', 'id')
    def projects(self):
        return project.Project
