from models.user import User

company = {
    'name': 'Staff Company',
    'address': 'Rivne, Ukraine'
}

user = {
    'username': 'admin',
    'email': 'admin@mail.com',
    'password': User.make_password('password'),
    'is_admin': True,
}
