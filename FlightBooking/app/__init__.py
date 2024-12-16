from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from datetime import datetime


# Database flight
app = Flask(__name__)
app.secret_key = 'DQ23QE@#e@@ef2#$v2#4@#Rcr2453#$2wedE1@EX1@E'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/flightbookingsystem?charset=utf8mb4" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["LIST_ALPHABET"] = [chr(i) for i in range(65, 91)]
app.config["NUMBER_STOP"] = {
    'Bay trực tiếp': 0,
    'Một điểm dừng': 1,
    'Hai điểm dừng': 2,
}
app.config["TIME_FLIGHT"] = {
    'Chuyến Bay Sáng' : 12,
    'Chuyến Bay Chiều': 18,
    'Chuyến Bay Tối': 24,
}
app.config["TICKET_CATEGORY"] ={
    "Phổ thông" : "PHOTHONG",
    "Thương gia" : "THUONGGIA"
}
app.config["TIME_NOW"] = datetime.now()

app.config["CHOOSE_TICKET_RETURN"] = False
db = SQLAlchemy(app)

# Database sub
app_sub = Flask(__name__)
app_sub.secret_key = 'ADA3DF3@#$233fW3SF#@$SDDF2!@#%'
app_sub.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/subdb?charset=utf8mb4" % quote("Admin@123")
app_sub.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app_sub.config["QUANTITY_TICKETS"] = 1
db_sub = SQLAlchemy(app_sub)

#API Cloudinary
cloudinary.config(cloud_name='dohsfqs6d',
                  api_key='171281981285222',
                  api_secret='2Ev1q24vbeTTFZMOOd6QxgLDB98')

# Đăng ký OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="181179286242-9rglc8esrv8a0qcju1e5nkvbdv0fi3hr.apps.googleusercontent.com",
    client_secret="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",
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile',
    },
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"  # Cung cấp metadata
)




login = LoginManager(app)
