from decouple import config


class Configurations:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = config('EMAIL_HOST')
    MAIL_PORT = config('EMAIL_PORT')
    MAIL_USE_TLS = config('EMAIL_USE_TLS')
    MAIL_USERNAME = config('EMAIL_HOST_USER')
    MAIL_PASSWORD = config('EMAIL_HOST_PASSWORD')