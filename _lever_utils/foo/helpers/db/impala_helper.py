# -*- coding:utf-8 -*-
import sqlalchemy
import pandas as pd
import sqlalchemy.orm as sqlalchemy_orm
from impala.dbapi import connect


class Db(object):
    _engine = None
    _session = None
    _configuration = None

    def __init__(self, *args, **kwargs):
        self._host = kwargs["host"]
        self._port = kwargs["port"]
        self._user = kwargs["user"] if "user" in kwargs else None
        self._password = kwargs["password"] if "password" in kwargs else None
        self._auth_mechanism = "NOSASL"

    def _creator(self):
        return connect(host=self._host,
                       port=self._port,
                       user=self._user,
                       password=self._password,
                       auth_mechanism=self._auth_mechanism)
    def creator(self):
        return connect(host=self._host,
                       port=self._port,
                       user=self._user,
                       password=self._password,
                       auth_mechanism=self._auth_mechanism)

    def init_engine(self):

        self._engine = sqlalchemy.create_engine('impala://', echo=True,
                                                creator=self._creator, max_overflow=100,
                                                pool_size=100, pool_timeout=180, )
        return self._engine

    def init_session(self):
        self._engine = self._engine if self._engine is not None else self.init_engine()
        self._session = sqlalchemy_orm.scoped_session(lambda: sqlalchemy_orm.create_session(bind=self._engine))()
        return self._session

    def get_engine(self):
        self._engine = self._engine if self._engine is not None else self.init_engine()
        return self._engine

    def get_session(self):
        self._session = self._session if self._session is not None else self.init_session()
        return self._session

    def execute(self, sql):
        try:
            self._engine = self._engine if self._engine is not None else self.init_engine()
            cursor = self._engine.execute(sql).cursor
            if cursor:
                columns = [metadata[0] for metadata in cursor.description]
                data = cursor.fetchall()
                df = pd.DataFrame(data=data, columns=columns)
                return df, None
            else:
                return None, None
        except Exception, e:
            return None, e

    def set_configuration(self, configuration):
        self._configuration = configuration

    def close(self):
        if self._session:
            self._session.close()


class Impala(Db):
    def __init__(self, *args, **kwargs):
        self._host = kwargs["host"]
        self._port = kwargs["port"] if "port" in kwargs else 21050
        self._user = kwargs["user"] if "user" in kwargs else None
        self._password = kwargs["password"] if "password" in kwargs else None
        # self._auth_mechanism = "PLAIN"
        self._auth_mechanism = "NOSASL"
