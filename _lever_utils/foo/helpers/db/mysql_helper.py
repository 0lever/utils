# -*- coding:utf-8 -*-
import sqlalchemy
import sqlalchemy.orm as sqlalchemy_orm
import pandas as pd
from sshtunnel import SSHTunnelForwarder


class Mysql(object):
    _engine = None
    _session = None
    _ssh_server = None

    def __init__(self, *args, **kwargs):
        user = kwargs["user"]
        password = kwargs["password"]
        host = kwargs["host"]
        port = kwargs["port"]
        db = kwargs["db"] if "db" in kwargs else ""

        is_ssh = kwargs["is_ssh"] if "is_ssh" in kwargs else False
        if is_ssh:
            ssh_host = kwargs["ssh_host"]
            ssh_post = kwargs["ssh_post"]
            ssh_user = kwargs["ssh_user"]
            ssh_password = kwargs["ssh_password"]
            self._ssh_server = SSHTunnelForwarder(
                (ssh_host, int(ssh_post)),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(host, int(port)))
            self._ssh_server.start()
            self._url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" \
                        % (user, password, '127.0.0.1', self._ssh_server.local_bind_port, db)
        else:
            self._url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (user, password, host, port, db)

    def init_engine(self):
        self._engine = sqlalchemy.create_engine(self._url, echo=False, encoding="utf-8")
        return self._engine

    def init_session(self):
        self._engine = self._engine if self._engine is not None else self.init_engine()
        self._session = sqlalchemy_orm.scoped_session(sqlalchemy_orm.sessionmaker(bind=self._engine))()
        return self._session

    def get_engine(self):
        self._engine = self._engine if self._engine is not None else self.init_engine()
        return self._engine

    def get_session(self):
        self._session = self._session if self._session is not None else self.init_session()
        return self._session

    def close(self):
        if self._session:
            self._session.close()
        if self._ssh_server:
            self._ssh_server.close()

    def execute(self, sql):
        try:
            if not self._engine:
                self.init_engine()
            result = self._engine.execute(sql)
            cursor = result.cursor
            if cursor:
                columns = [metadata[0] for metadata in cursor.description]
                data = cursor.fetchall()
                data = list(data)
                df = pd.DataFrame(data=data, columns=columns)
                return df, None
            else:
                return None, None
        except Exception, e:
            return None, e
