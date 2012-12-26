GalTrace
========

This project is used to trace my interested galgames. It records each game's
release date, and my playing status.

This is a `Django`_ project and currently hosting on `Heroku`_.

Dependencies
------------

* `Python`_ >= 2.7
* `Django`_ >= 1.4
* `PycURL`_
* `PyQuery`_
* `bpssl`_ (for production, but necessary)
* `Gunicorn`_ >= 0.15 (production only)
* `gevent`_ (production only)
* `Psycopg`_ (production only)
* `DJ-Database-URL`_ (production only)

How To Upload Private Settings
------------------------------

.. code:: bash 

  # ensure your **galtrace/private/data.json** exists, see below section
  python galtrace/private/settings.py

Note
----

``user_env_compile`` must turns on to let `Heroku`_ collect static assets. For
more information, please see `Django and Static Assets | Heroku Dev Center`_.

I use `Google API`_ to send emails on `Heroku`_.
Please create an **installed application** client ID, then set
``GOOGLE_API_CLIENT_ID`` and ``GOOGLE_API_CLIENT_SECRET`` in
``galtrace/private/data.json`` respectively.
Follow `oauth2.py example`_ to gain a **refresh token**, and save the token as
``EMAIL_HOST_PASSWORD``.

This project doesn't provide registering right now.

Development configuration will read ``galtrace/private/data.json``, which is
encrypted by my private gpg key. You must create your own one.

.. _bpssl: https://bitbucket.org/beproud/bpssl/
.. _DJ-Database-URL: https://github.com/kennethreitz/dj-database-url
.. _Django: https://www.djangoproject.com/
.. _Django and Static Assets | Heroku Dev Center: https://devcenter.heroku.com/articles/django-assets
.. _gevent: http://www.gevent.org/
.. _Google API: https://code.google.com/apis/console/
.. _Gunicorn: http://gunicorn.org/
.. _Heroku: http://www.heroku.com/
.. _oauth2.py example: http://code.google.com/p/google-mail-oauth2-tools/wiki/OAuth2DotPyRunThrough
.. _Psycopg: http://initd.org/psycopg/
.. _PycURL: http://pycurl.sourceforge.net/
.. _PyQuery: https://github.com/gawel/pyquery
.. _Python: http://www.python.org/
