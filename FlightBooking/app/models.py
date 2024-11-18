from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.operators import truediv

from app import db, app, db_sub
import hashlib
from enum import Enum as RoleEnum
from flask_login import UserMixin


# Database subdb
class CategoryPage(db_sub.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    ico = Column(String(100), nullable=True)


# Database Flight Booking System
class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True, default="https://res.cloudinary.com/dohsfqs6d/image/upload/v1731589856/ewqzzku2a2fcczgumnzf.jpg")
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def get_id(self):
        return self.id


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        # u = User(name="admin", username="admin", password=str(hashlib.md5("cuong2004".encode('utf-8')).hexdigest()),
        #          avatar="https://res.cloudinary.com/dohsfqs6d/image/upload/v1731589856/ewqzzku2a2fcczgumnzf.jpg",
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        db_sub.create_all()
        c1 = CategoryPage(name='Trang chủ')
        c2 = CategoryPage(name='Giới thiệu')
        c3 = CategoryPage(name='Dịch vụ')
        c4 = CategoryPage(name='Khuyến mãi')
        c5 = CategoryPage(name='Liên hệ')

        db_sub.session.add_all([c1, c2, c3, c4, c5])
        db_sub.session.commit()
