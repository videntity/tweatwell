Tweatwell: Food Tracking Microblog Game
Copyright 2011 Videntity Systems, Inc.
===========================================

Tweatwell is a web-based food microblog tracking game written in Django.

Its goal is to encourage a plant based diet amongsst a college
student population.

Tweatwell supports group-tracking and self-tracking of diet information and 
uses OMHE Microsyntax to encode food entry. You can tweat what you eat
and Tweatwell will automatically capture this information and add it to your
food blog. Tweatwell only reads tweets with a specific has tag defined in the
settings file. The basic commands supported by tweatwell are as follows:

======= ========= ============================= ==============
COMMAND ALIASES   ACCEPTABLE VALUES             OPTIONS
======= ========= ============================= ==============
frv     freggie   fruit or veggie from list     quantity 1-10 
ci      comment   Free text                     N/A
======= ========= ============================= ==============


Eat Healthy, Live Long, and TweatWell.


Installation:
=============

Tweatwell is written in Python 2.6 and Django 1.2.4 and has some other
dependencies. Note that depending on your operating system or distribution
some of these dependencies may already be installed. Tweatwell dependicies are
as follows:

* Python 2.7
* Django 1.3.1 - http://djangoproject.org
* RESTCat* - http://github.com/videntity/RESTCat
* python-omhe: http://github.com/videntity/python-omhe
* django-avatar version 1.0 - The Python Image Lib is needed for this
* PIL -Python Imaging Library
* Pycurl: Curl and the Python bindings for libcurl

RESTCat is the backend RESTFul engine for data storage, security, and sharing. 
This usually should run on a seperate server in a production environment but it
doesn't have to if the application is small.

Here is a quickstart guide to get you going. 
::
    git clone git://github.com/aviars/tweatwell.git
    git clone git://github.com/aviars/RESTCat.git
    sudo easy_install pip
    cd tweatwell
    sudo pip install -r config/requirements.txt

Running the Development Server:
===============================

Here's how to create the database and start the Django's devlopment server environment.
::
    sudo apt-get install git-core python-imaging build-essential python-setuptools memcached libmemcached-dev

::
    sudo easy_install pip

::
    cd config
    sudo pip install -r requirements.txt

::
    cd tweatwell
    python manage.py syncdb
    python manage.py runserver

Now  point your browser to http://127.0.0.1:8000 and you should see the startup page.
Note you will need to adjust some settings in settings.py for your own environment.
These mainly include your email server, RESTCAT server, and database server settings.


Production Django configuration is beyond the scope of these setup instructions, but great
documentation may be found online. Please see the Django documentation  at
http://djangoproject.org for more information. IF YOU RUN RESTCAT AND tweatwell
WITHOUT SSL/HTTPS YOU DO SO AT YOUR OWN RISK!  


You may use any database that is supported by Django.  These include PostgreSQL,
MySQL, SQLite, and Oracle.  the default is SQLite

License:
========
Tweatwell is avaliable under a dual license. You may use either GPL or a
commercial license.  You may use this software for free under the GPL for 
educational and non-profit activities only.  If you want
to use this software, its direvative works, for commercial purposes you must
use the commercial license agreement.  The commercial license comes with support
and allows greater freedoms than the GPL.
