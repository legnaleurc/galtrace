GalTrace
========

|build status|_

This project is used to trace my interested galgames. It records each game's
release date, and my playing status.

This is a `Django`_ project and currently hosting on `Heroku`_.

Dependencies
------------

* common

  * `Python`_ >= 2.7
  * `Django`_ >= 1.4
  * `PycURL`_
  * `PyQuery`_

* production (for `Heroku`_)

  * `bpssl`_
  * `Gunicorn`_ >= 0.15
  * `gevent`_
  * `Psycopg`_
  * `DJ-Database-URL`_

Special Commands
----------------

Upload Private Settings
~~~~~~~~~~~~~~~~~~~~~~~

Avaliable in ``galtrace.settings.development``

Precondition: ``galtrace/settings/secret.json`` exists.
For more information, please see Notes_.

.. code:: bash

  python manage.py gt_push

Test
~~~~

Avaliable in ``galtrace.settings.development``

.. code:: bash

  python manage.py gt_test

Notes
-----

I use `Google API`_ to send emails on `Heroku`_.
Please create an **installed application** client ID, then set
``GOOGLE_API_CLIENT_ID`` and ``GOOGLE_API_CLIENT_SECRET`` in
``galtrace/settings/secret.json`` respectively.
Follow `oauth2.py example`_ to gain a **refresh token**, and save the token as
``EMAIL_HOST_PASSWORD``.

This project doesn't provide registering right now.

Development configuration will read ``galtrace/settings/secret.json``, which is
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

.. Travis CI
.. _build status: https://travis-ci.org/legnaleurc/galtrace
.. |build status| image:: https://travis-ci.org/legnaleurc/galtrace.png
