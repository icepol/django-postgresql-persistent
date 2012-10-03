from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as PGDatabaseWrapper
from django.db.utils import DatabaseError


class DatabaseWrapper(PGDatabaseWrapper):
    def _cursor(self):
        # check the name of the DB becouse if tests is runnig it will change
        _name = getattr(self, '_name', None)
        if _name is None:
            self._name = self.settings_dict['NAME']

        if _name != self.settings_dict['NAME']:
            # databasename was changed
            self.connection = None
            self._name = self.settings_dict['NAME']

        _connected = getattr(self, '_connected', None)
        if _connected is None:
            try:
                # make simple query
                cursor = super(DatabaseWrapper, self)._cursor()
                cursor.execute('SELECT 1')
            except DatabaseError:
                # connection is down, this will reconnect database
                self.connection = None
                cursor = super(DatabaseWrapper, self)._cursor()
        else:
            # this is another query in this request, just return cursor
            cursor = super(DatabaseWrapper, self)._cursor()

        self._connected = True
        return cursor

    def close(self):
        if self.connection is not None:
            self.connection.commit()

        self._connected = None
