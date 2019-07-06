import string

import pymysql.cursors
from config import host, user, password, db
import re
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class Shelf(Base):
    __tablename__ = 'shelf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    author_name = Column(String(30))
    book_name = Column(String(30))
    book_desc = Column(String(428))
    book_cover_url = Column(String(400))
    recent_chapter_url = Column(String(140))
    last_update_at = Column(String(40))
    classify_name = Column(String(40))
    novel_id = Column(Integer())


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    email = Column(String(30), nullable=True)
    gender = Column(Integer, default=0)
    password = Column(String(128), nullable=False)
    phone = Column(String(11))

    # # 定义密码哈希加密
    # @property
    # def password(self):
    #     return self.password
    #
    # def generate_password(self, raw):
    #     self.password = generate_password_hash(raw)
    #
    # # 验证密码
    # def check_password(self, raw):
    #     return check_password_hash(self.password, raw)


class Chapter(Base):
    __tablename__ = 'gysw_chapter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500))
    name = Column(String(200))
    novel_id = Column(Integer)


class Novel(Base):
    __tablename__ = 'gysw_novel'

    url = Column(String(50))
    book_name = Column(String(50))
    author_name = Column(String(20))
    classify_id = Column(Integer)
    id = Column(Integer, primary_key=True, autoincrement=True)


class Classify(Base):
    __tablename__ = 'gysw_classify'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(50))
    desc = Column(String(20))


class Db(object):
    def __init__(self):
        self.connection = pymysql.connect(host=host,
                                          user=user, password=password, db=db,
                                          charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, use_unicode=True,
                                          autocommit=True
                                          )
        # self.creatTable("gysw_classify")
        # self.creatTable('gysw_chapter')
        # self.creatTable('gysw_novel')
        # self.connection.set_character_set('utf8')

        # 初始化数据库连接:
        engine = create_engine('mysql+pymysql://root:111111@localhost:3306/xiaoshuo?charset=utf8', echo=True,
                               encoding='utf-8', convert_unicode=True)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        # self.session.execute('SET NAMES utf8;')
        # self.session.execute('SET CHARACTER SET utf8;')
        # self.session.execute('SET character_set_connection=utf8;')
        Base.metadata.create_all(engine)

    def createDb(self):
        sql = 'create database awesome character set utf8'
        with self.connection.cursor() as  cursor:
            cursor.execute(sql)

    def table_exits(self, con: pymysql.cursors.DictCursor, table_name):

        sql = 'show tables'
        con.execute(sql)
        tables = [con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            print(table_name)
            return 1
        else:
            return 0

    @staticmethod
    def create_table(self, table_name):
        table_name = table_name
        structs = [
            {'fieldname': 'id', 'type': 'varchar2(50)', 'primary': True, 'default': ''},
            {'fieldname': 'PROJECTNUMBER', 'type': 'varchar2(50)', 'default': 0, 'isnull':
                True}]
        self.con(table_name, structs)

    def creatTable(self, table_name):
        if (self.table_exits(self.connection.cursor(), table_name) != 1):
            print("表不存在 ,")
            with self.connection.cursor() as cursor:
                sql = """CREATE  TABLE  %s (`path`CHAR(40) not null ,`desc` CHAR(20) )"""
                # sql = """CREATE TABLE gysw_classify (
                #          `path`  CHAR(20) NOT NULL,
                #          `desc`  CHAR(20),
                #          AGE INT,
                #          SEX CHAR(1),
                #          INCOME FLOAT )"""
                cursor.execute(sql, table_name)

    def insertOne(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)

    def insertMany(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(sql, params)
            self.connection.commit()
        except Exception as e:
            print('------sql cuo  wu ', e)
            self.connection.rollback()

    def selectOne(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(e)

    def selectAll(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(e)

    def removeOne(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)

    def updateOne(self, sql, params=()):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)

    def close(self):
        self.connection.close()

    def getClassify(self):
        classifys = self.session.query(Classify).all()
        return classifys


def test():
    db = Db()
    # db.insertOne('insert into gysw_classify (`path`, `desc` ) values (%s, %s)', ("xiuzhenxiaoshuo", "修真小说"))
    # result = db.selectAll('select * from gysw_classify')
    # db.close()
    # print(result)


if __name__ == '__main__':
    test()
