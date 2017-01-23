import unittest
import os
os.system('yes '' | python test_db.py migrate')
os.system('yes '' | python test_db.py migrate:reset')
os.system('yes '' |python test_db.py migrate')


suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(suite)
