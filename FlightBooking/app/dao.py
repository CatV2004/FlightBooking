from app.models import User
from app import app, db
import hashlib
import cloudinary.uploader



def add_or_get_user_from_google(name, username):
    user = User.query.filter_by(username=username).first()
    if not user:
        try:
            user = User(name=name, username=username, password="")
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(f"Error while adding user: {ex}")
            raise ex
    return user


def add_user(name, username, password):
    try:
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

        u = User(name=name, username=username, password=password)
        db.session.add(u)
        db.session.commit()
    except Exception as ex:
        db.rollback()
        print(f"Error: {ex}")
        raise ex


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


def get_user_by_id(id):
    return User.query.get(id)

#kiểm tra username có tồn tại không
def is_username_exists(username):
    return User.query.filter(User.username.__eq__(username)).first() is not None