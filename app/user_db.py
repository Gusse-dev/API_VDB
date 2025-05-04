from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "HTRH7485WGWEGHWER754EWG75EQGW5"
ALGORITHM = "HS256"

user_db = { "john":{ 
            'username': 'john',
            'hashed_password': pwd_context.hash("doe")
            },
            "max":{
            'username': 'max',
            'hashed_password': pwd_context.hash("musterman")
            },
            "jane":{
            'username': 'jane',
            'hashed_password': pwd_context.hash("citizen")
            }
          }