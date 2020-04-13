import requests
import psycopg
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# 1. POST an HTTP request with a valid expression to the server.
# Examine the response and confirm that the correct answer is returned.
r = requests.post(url = 'http://192.168.99.100/add', data = {'expression': 'a + 1'})
assert r.status_code == 200

# Q2 Establish a connection to the database directly and verify that the string you sent
# has been correctly stored in the database. For this step, you can use SQLAlchemy, or
# write the SQL directly if you prefer, however note that this is a postgres database
# which does have subtly different syntax from sqlite. (For simple queries this shouldn't be a big issue.)

DATABASE_URI = 'postgres+psycopg2://cs162_user:cs162_password@192.168.99.100:5432/cs162'
Session = sessionmaker(bind=engine)
metadata = MetaData(engine)
expressions = Table('expression', metadata, autoload=True)

s = Session()

# 3. POST an HTTP request with an invalid expression to the server.
# Examine the response and confirm that an error is raised.
r = requests.post(url = 'http://192.168.99.100/add', data = {'expression': '1 + 1'})
assert r.status_code == 500


# Q4 Confirm that no more rows have been added to the database since the last valid
# expression was sent to the server. (For the purposes of this class, you can assume
# that no-one else is accessing the database while the tests are running.)
exps = s.query(expressions).all()
for i in range(len(exps)):
    print('{} = {}'.format(exps[i].text, exps[i].value))