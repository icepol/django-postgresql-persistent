django-python-persistent
========================

Simple django postgresql_psycopg2 wrapper to create postgresql persistent connection.

## Installation
pip install -e git://github.com/icepol/django-postgresql-persistent.git#egg=django_postgresql_persistent

## Why to use it?
Every database connection take some time. It would be tens of milisecond, especially if the database is on another another server and not locally.<br />
You can save this time and speed each request.<br />

## How to use it?
Just set up this database backend in your settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_postgresql_persistent',
        'NAME': '...',
        'USER': '...',
        'PASSWORD': '...',
        'HOST': '...',
        'PORT': '5432',
    }
}
```