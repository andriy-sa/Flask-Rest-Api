from orator.seeds import Seeder
from models.user import User
from models.company import Company


class DatabaseSeeder(Seeder):
    def run(self):
        """
        Run the database seeds.
        """
        # create staf company
        company = Company.create({
            'name': 'Staff Company',
            'address': 'Rivne, Ukraine'
        })

        # create User 1
        user = User()
        user.username = 'admin'
        user.email = 'andriy_smolyar_0@mail.ru'
        user.password = User.make_password('password')
        user.is_admin = True
        user.company_id = company.id
        user.save()

        # create User 2
        user = User()
        user.username = 'user'
        user.email = 'user@mail.ru'
        user.password = User.make_password('password')
        user.is_admin = False
        user.company_id = company.id
        user.save()
