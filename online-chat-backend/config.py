SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Pvzheroes125@localhost:3306/chat_db?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True
# SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_SIZE = 1024
SQLALCHEMY_POOL_TIMEOUT = 90
SQLALCHEMY_POOL_RECYCLE = 3
SQLALCHEMY_MAX_OVERFLOW = 1024

JSON_AS_ASCII = False
JSONIFY_MIMETYPE = "application/json;charset=utf-8"
