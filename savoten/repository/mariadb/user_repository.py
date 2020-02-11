from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

from savoten.domain import User
from savoten.domain import UserRepositoryInterface

# Baseというメタクラスを作って、テーブル定義に使いたいクラスの継承させる
Base = declarative_base()

class OrmUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    permission = Column(Integer)
    email = Column(String(255))
    created_at = Column(DateTime(timezone=False))
    updated_at = Column(DateTime(timezone=False))
    deleted_at = Column(DateTime(timezone=False))

class UserRepository(UserRepositoryInterface):

    def __init__(self):

        url = 'mysql+pymysql://python:python@db/SAVOTEN'
        engine = create_engine(url, echo=False)
        # Baseクラスを継承させて作ったクラスのテーブルが作成される
        Base.metadata.create_all(engine)
        # セッションの作成
        Session = orm.sessionmaker(bind=engine)
        self.session = Session()

    def _user_to_orm_user(self, user):
        return OrmUser(id=user.id,name=user.name, permission=user.permission, email=user.email, created_at=user.created_at, updated_at=user.updated_at, deleted_at=user.deleted_at)

    def _orm_user_to_user(self, orm_user):
        return User(id=orm_user.id,name=orm_user.name, permission=orm_user.permission, email=orm_user.email, created_at=orm_user.created_at, updated_at=orm_user.updated_at, deleted_at=orm_user.deleted_at)

    def save(self, user):
#        if user.id is None:
#            user.id = self._get_new_id()
        #self.users[user.id] = user
        orm_user = self._user_to_orm_user(user)
        self.session.add(orm_user)
        self.session.commit()
        saved_user = self._orm_user_to_user(orm_user)
        return saved_user

    def delete(self, user):
        if user.id is None or user.id not in self.users:
            raise ValueError("error!")
        self.users.pop(user.id)

    def find_by_id(self, id):
        return self.users.get(id, None)

    def find_all(self):
        return self.users.values()

#    def _get_new_id(self):
#        self.id = self.id + 1
#        return self.id
