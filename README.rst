GalTrace
========

This project is intend to trace my interested galgames. It records game's
release date, and my playing status.

This is a `Django`_ project and is hosting on `Heroku`_ currently.

Dependencies
------------

* `Python`_ >= 2.7
* `Django`_ >= 1.4
* `PycURL`_
* `PyQuery`_
* `Gunicorn`_
* `Psycopg`_ (only needed on production)
* `gevent`_ (only needed on production)
* `DJ-Database-URL`_ (only needed on production)

How To Upload Private Settings
------------------------------

::

    # ensure your **galtrace/private/data.json** exists
    python galtrace/private/settings.py

Note
----

This project doesn't provide registering right now.

Development configuration will read **galtrace/private/data.json**, which is
encrypted by my private gpg key. You must create your own one.

.. _DJ-Database-URL: https://github.com/kennethreitz/dj-database-url
.. _Django: https://www.djangoproject.com/
.. _gevent: http://www.gevent.org/
.. _Gunicorn: http://gunicorn.org/
.. _Heroku: http://www.heroku.com/
.. _Psycopg: http://initd.org/psycopg/
.. _PycURL: http://pycurl.sourceforge.net/
.. _PyQuery: https://bitbucket.org/olauzanne/pyquery/
.. _Python: http://www.python.org/
