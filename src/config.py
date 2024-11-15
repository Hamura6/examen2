import pymysql
class Config:
    MYSQL_HOST='localhost'
    MYSQL_DB='exmen2'
    MYSQL_USER='root'
    MYSQL_PASSWORD=''
def db_connection(app):
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        database=app.config['MYSQL_DB'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
    )