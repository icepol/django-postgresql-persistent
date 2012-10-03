from distutils.core import setup

VERSION = '1.0'

setup(
    name='django-postgresql-persistent',
    version=VERSION,
    description='Simple django postgresql_psycopg2 wrapper to create postgresql persistent connection.',
    author='Pavel Koci',
    author_email='pavel.koci@icepol.net',
    packages=['django_postgresql_persistent'],
)
