import os

class Config():
    SECRET_KEY = "f4fa483fa875f9cbf287dac5e6f36f006cd889289913d1698007df55cd9898cd"
    SECURITY_PASSWORD_SALT = "317253998663595341291509795129662632201"
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    WTF_CSRF_ENABLED = False
    POSTER_FOLDER = os.path.join('zoo', 'static', 'posters')
    SECURITY_SEND_REGISTER_EMAIL = False
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = 'redis://localhost:6379/3'