# -*- coding:utf-8 -*-
from impala_helper import Db
import pandas as pd

class Hive(Db):
    def __init__(self, *args, **kwargs):
        self._host = kwargs["host"]
        self._port = kwargs["port"] if "port" in kwargs else 10000
        self._user = kwargs["user"] if "user" in kwargs else None
        self._password = kwargs["password"] if "password" in kwargs else None
        # self._auth_mechanism = "LDAP"
        self._auth_mechanism = "PLAIN"

    def execute(self, sql, is_ddl=True):
        try:
            self._engine = self._engine if self._engine is not None else self.init_engine()
            cursor = self._engine.execute("select 1").cursor

            cursor.execute(sql, configuration=self._configuration)
            if is_ddl:
                return None, None

            if cursor:
                columns = [metadata[0] for metadata in cursor.description]
                data = cursor.fetchall()
                df = pd.DataFrame(data=data, columns=columns)
                return df, None
            else:
                return None, None
        except Exception, e:
            return None, e