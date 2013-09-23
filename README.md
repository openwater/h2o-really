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
* `pip install -r requirements.txt`
* Set up PostGIS with hstore

  Outside your virtual environment, if you haven't ever installed GDAL before:

        sudo pip install numpy
        brew update
        brew install gdal


  For those on Mac OS X, we recommend using `Postgres.app`. In order to enable
  the spatial element, simply create a database (let’s call it h2o\_really) and then
  enable the spatial element:

        createdb -h localhost h2o_really && psql -h localhost h2o_really
  
  Then you need the hstore and postgis extensions:

        h2o_really=# CREATE EXTENSION hstore;
        h2o_really=# CREATE EXTENSION postgis;
  
  In theory, that’s it...

  Note that we do -h localhost because the Postgres.app is not using the normal
  sockets approach, rather it binds to 0.0.0.0 (or 127.0.0.1 by default I
  think) on port 5432. If you’re using linux then probably you don’t need that
  bit.
  
  Get out of the Postgres shell (Ctrl+D) and then:
  
* `./manage.py syncdb`
* `./manage.py migrate`
* `./manage.py runserver 127.0.0.1:8080`

* Browse to http://127.0.0.1:8080 in a browser!
  
* Add/fix/commit stuff on a branch
* Submit a pull request

Load initial data
-----------------

Use the `load_gqahi_nutrients` management command to load the initial data sets, e.g.:

    ./manage.py load_gqahi_nutrients data/GQAHI_Nutrients/nitrate\ GQA\ grades\ 2009\ \(Wales\).csv --nutrient N

and likewise for the three other CSV files in the data directory (use P as the nutrient argument for Phosphates).

Browse the API
--------------
After loading some data, you should be able to browse the API at, e.g.:

http://127.0.0.1:8000/api/v1/observations/measurements/

See `openwater/urls.py` and `observations/api/urls.py` for more information.

Browse the data
---------------
In order for the interactive maps to work, you will need to register for an API key from CloudMade (http://cloudmade.com/).
Once you have a key, include it in your local settings as `CLOUDMADE_API_KEY`.

With that set up you should be able to visit the map page and see some nice clustered observations:

http://127.0.0.1:8000/observations/map/
