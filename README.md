Tweatwell: Food Tracking Microblog Game
=======================================

Copyright 2011-2015 Videntity Systems, Inc.


Tweatwell is a web-based food microblog tracking game written in Django.
The goal of the game is to encourage a plant based diet amongst a college
student population. Eat Healthy, Live Long, and Tweat Well.


Installation:
=============

Tweatwell is written in Python 2.7 and Django 1.6.1 and has some other
dependencies.

Here is a quickstart guide to setup a development environment. 


    sudo apt-get install git-core python-dev python-imaging build-essential python-pip memcached libmemcached-dev zlib1g-dev
    git clone git://github.com/aviars/tweatwell.git
    cd tweatwell
    sudo pip install -r tweatwell/requirements.txt


Running the Development Server:
===============================

Here's how to create the database and start the Django's devlopment server
environment.  You should also use virtualenv and virtualenvwrapper when
developing in Python.



    python manage.py syncdb
    python manage.py runserver

Now  point your browser to http://127.0.0.1:8000 and you should see the startup
page. Note you will need to adjust some settings in settings.py for your own
environment.  These mainly include your email and database server settings. You
may use any database that is supported by Django.  These include PostgreSQL,
MySQL, SQLite, and Oracle.  The default is SQLite.


Production Configuration using Apache and modWSGI
=================================================
Production Django configuration can be done in many ways and an exhaustive
explanation is beyond the scope of these setup instructions.  The information
provided here is just provided as a quick jumpstart. More detailed documentation
may be found at http://djangoproject.org.  


    sudo apt-get install apache2 libapache2-mod-wsgi
    cd tweatwell
    cp config/settings_local.py .

You need to modify the file '/etc/apache2/sites-available/default'. You need to
add this line to the VirtualHost on which you want to run the application.


    WSGIScriptAlias / /home/ubuntu/django-apps/tweatwell/config/apache/django.wsgi

If you are using SQLite, make sure the db folder is readable and writeable by
the webserver.


    cd tweatwell
    python manage.py syncdb
    sudo chmod -R 777 db

Restart the Apache webserver:


    sudo apache2ctl restart

License:
========

Tweatwell has a dual license. You may use either GPL or a
commercial license.  You may use this software for free under the GPL for 
educational and non-profit activities only.  If you want to use this software, or
it's derivative works, for commercial purposes, you must use the commercial
license agreement.  The commercial license comes with support and allows greater
freedoms than the GPL.
