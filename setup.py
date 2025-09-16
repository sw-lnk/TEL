from getpass import getpass
from sqlmodel import select

from tel.user.models import User
from tel.database import get_session, init_database
from tel.authentification.utils import get_password_hash


init_database()

print('Setup TEL')
print('Create Superuser...')

while True:
    username = input('Username: ')
    with get_session() as session:
        user_db = session.exec(select(User).where(User.username == username)).first()
        
        if not user_db:
            break
        
        print(f'Username: {username} already exists')
        
first_name = input('First Name: ')
last_name = input('Last Name: ')

while True:
    pwd1 = getpass('User Password: ')
    pwd2 = getpass('Confirm Password: ')
    if pwd1 == pwd2:
        break
    
    print('Password is not matching.')
    
email = input('E-Mail: ')
    
user = User(
    username=username,
    first_name=first_name,
    last_name=last_name,
    hashed_password=get_password_hash(pwd1),
    email=email,
    is_active=True,
    is_superuser=True,
)
with get_session() as session:
    session.add(user)
    session.commit()
    session.refresh(user)

print('Creating User successful.')
