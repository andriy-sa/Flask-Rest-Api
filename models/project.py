from orator import Model
from orator.orm import belongs_to
from models import company


class Project(Model):
    __fillable__ = ['title', 'description', 'price', 'published', 'longitude', 'latitude', 'company_id']

    def get_date_format(self):
        return '%d-%m-%Y %H:%M:%S'

    @belongs_to('company_id', 'id')
    def company(self):
        return company.Company
