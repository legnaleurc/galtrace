GalTrace
========

This project is intend to trace my interested galgames. It records game's
release date, and my playing status.

This is a `Django`_ project and currently host on `Heroku`_.

Dependencies
------------

* `Python`_ >= 2.7
* `Django`_ >= 1.4
* `PycURL`_
* `PyQuery`_
* `bpssl`_ (for production, but necessary)
* `Gunicorn`_ (for production, but necessary)
* `gevent`_ (production only)
* `Psycopg`_ (production only)
* `DJ-Database-URL`_ (production only)

How To Upload Private Settings
------------------------------

::

    # ensure your **galtrace/private/data.json** exists
    python galtrace/private/settings.py

Note
----

`Heroku`_ won't collectstatic if **user_env_compile** turns off somehow.

This project doesn't provide registering right now.

Development configuration will read **galtrace/private/data.json**, which is
encrypted by my private gpg key. You must create your own one.

.. _bpssl: https://bitbucket.org/beproud/bpssl/
.. _DJ-Database-URL: https://github.com/kennethreitz/dj-database-url
.. _Django: https://www.djangoproject.com/
.. _gevent: http://www.gevent.org/
.. _Gunicorn: http://gunicorn.org/
.. _Heroku: http://www.heroku.com/
.. _Psycopg: http://initd.org/psycopg/
.. _PycURL: http://pycurl.sourceforge.net/
.. _PyQuery: https://bitbucket.org/olauzanne/pyquery/
.. _Python: http://www.python.org/
