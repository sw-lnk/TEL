from getpass import getpass

from tel.user.models import User
from tel.database import get_session, init_database
from tel.authentification.utils import get_password_hash


init_database()

print('Setup TEL')
print('Create Superuser...')

username = input('Username: ')

while True:
    pwd1 = getpass('User Password: ')
    pwd2 = getpass('Confirm Password: ')
    if pwd1 == pwd2:
        break
    
    print('Password is not matching.')
    
email = input('E-Mail: ')
    
user = User(
    username=username,
    hashed_password=get_password_hash(pwd1),
    email=email,
    is_active=True,
    is_superuser=True
)
with get_session() as session:
    session.add(user)
    session.commit()
    session.refresh(user)

print('Creating User successful.')
