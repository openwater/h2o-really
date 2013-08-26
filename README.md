H₂O Really?
===========

http://h2o-really.co.uk

H₂O Really? aims to set up a very basic monitoring database for water quality.
Data can be captured by anyone, concerning any water quality parameter, and is
available to anyone (i.e. this is an open data project).

Contributing
------------

If you want to help out:

* Check out this repo
* Make a virtualenv (e.g. `mkvirtualenv h2o_really`)
* `pip install requirements.txt`
* Set up PostGIS with hstore

  Outside your virtual environment, if you haven't ever installed GDAL before:

        sudo pip install numpy
        brew update
        brew install gdal


  For those on Mac OS X, we recommend using `Postgres.app`. In order to enable
  the spatial element, simply create a database (let’s call it h2o\_really) and then
  enable the spatial element:

        createdb -h localhost h2o_really && psql -h localhost h2o_really
        h2o_really=# CREATE EXTENSION postgis;
  
  Then you need the hstore extension:

        h2o_really=# CREATE EXTENSION hstore;
  
  In theory, that’s it...

  Note that we do -h localhost because the Postgres.app is not using the normal
  sockets approach, rather it binds to 0.0.0.0 (or 127.0.0.1 by default I
  think) on port 5432. If you’re using linux then probably you don’t need that
  bit.
* `./manage.py syncdb`
* `./manage.py migrate`
* Add/fix/commit stuff on a branch
* Submit a pull request
