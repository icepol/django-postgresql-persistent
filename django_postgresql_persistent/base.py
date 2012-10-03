"""
Simple Django database wrapper based on postgresql_psycopg2.
In base wrapper every http request opens own database connection at the start
and close this connection at the end of the request.
This wrapper implements mechanism which keeps this connection open.
"""
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as PGDatabaseWrapper
from django.db.utils import DatabaseError


class DatabaseWrapper(PGDatabaseWrapper):
    """
    Simple Django database wrapper based on postgresql_psycopg2.
    """
    def _cursor(self):
        # check the name of the DB
        # if tests is runnig it will be changed
        _name = getattr(self, '_name', None)
        if _name is None:
            self._name = self.settings_dict['NAME']

        if _name != self.settings_dict['NAME']:
            # database name was changed
            self.connection = None
            self._name = self.settings_dict['NAME']

        _connected = getattr(self, '_connected', None)
        if _connected is None:
            # this is first query in this http request
            try:
                # make simple query
                cursor = super(DatabaseWrapper, self)._cursor()
                cursor.execute('SELECT 1')
            except DatabaseError:
                # connection is down, this will reconnect database
                self.connection = None
                cursor = super(DatabaseWrapper, self)._cursor()

            # mark this connectio as open
            self._connected = True
        else:
            # this is another query in this request, just return cursor
            cursor = super(DatabaseWrapper, self)._cursor()

        return cursor

    def close(self):
        if self.connection is not None:
            # if there is connection, commit all transaction
            self.connection.commit()

        # at the end of the request mark this connection as closed
        self._connected = None
