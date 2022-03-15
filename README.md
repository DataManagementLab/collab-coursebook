# Collab Coursebook

![Django CI](https://github.com/DataManagementLab/collab-coursebook/workflows/Django%20CI/badge.svg)

## Description

Collab Coursebook is a platform for collaborative learning und knowledge organization. It provides a place to share and re-use notes and other learning materials.

## Setup

This repository contains a Django project with several apps.


### Requirements

Collab Coursebook has two types of requirements: System requirements are dependent on operating system and need to be installed manually beforehand. Python requirements will be installed inside a virtual environment (strongly recommended) during a setup.


#### System Requirements

* Python 3.7+ incl. development tools
* Virtualenv
* poppler
* TeX Distribution (e.g. TeX Live)
* For production using uwsgi:
  * C compiler e.g. gcc
  * uwsgi
  * uwsgi Python3 plugin
* For production using Apache (in addition to uwsgi)
  * the mod proxy uwsgi plugin for apache2

#### Python Requirements

Python requirements are listed in ``requirements.txt``. They can be installed with pip using ``-r requirements.txt``.


#### Distributable Setup

* In order to use Nestable2 correctly the dist folder is needed. This folder can be found here: https://github.com/RamonSmit/Nestable2
    * The folder must be placed in `frontend/static/vendor/Nestable2`.
### Development Setup

* Create a new directory that should contain the files in the future, e.g. ``mkdir collab-coursebook``
* Change into that directory ``cd collab-coursebook``
* Clone this repository ``git clone URL .``


#### Linux

**Automatic Setup**

1. Execute the setup bash script ``utils/setup.sh``

**Manual Setup**

1. Set up a virtual environment using the proper python version ``virtualenv venv -p python3``
1. Activate virtualenv ``source venv/bin/activate``
1. Install python requirements ``pip install -r requirements.txt``
1. Set up necessary database tables etc. ``python manage.py migrate``
1. Setup initial revision for all registered models for versioning``python manage.py createinitialrevisions``
1. Prepare static files (can be omitted for dev setups) ``python manage.py collectstatic``
1. Compile translations ``python manage.py compilemessages``
1. Create a privileged user, credentials are entered interactively on CLI ``python manage.py createsuperuser``
1. Deactivate virtualenv ``deactivate``
1. Create the file ``collab_coursebook/settings_secrets.py`` (copy from ``settings_secrets.py.sample``) and fill in the YouTube API key

**Development Server**

To start the application for development use ``python manage.py runserver 0:8000`` from the root directory.
*Do not use this for deployment!*

In your browser, access ``http://127.0.0.1:8000/`` and continue from there.

#### Windows

**Manual Setup**

1. Set up a virtual environment using the proper python version ``virtualenv venv -p python3``
1. Activate virtualenv `.\venv\Scripts\activate`
1. Install python requirements ``pip install -r requirements.txt``
1. Install python magic-bin ``pip install python-magic-bin``
1. Set up necessary database tables etc. ``python manage.py migrate``
1. Setup initial revision for all registered models for versioning``python manage.py createinitialrevisions``   
1. Prepare static files (can be omitted for dev setups) ``python manage.py collectstatic``
1. Compile translations ``python manage.py compilemessages``
1. Create a privileged user, credentials are entered interactively on CLI ``python manage.py createsuperuser``
1. Deactivate virtualenv ``deactivate``
1. Create the file ``collab_coursebook/settings_secrets.py`` (copy from ``settings_secrets.py.sample``) and fill in the YouTube API key for development regarding YouTube Videos

**Development Server**

To start the application for development use ``python manage.py runserver 0.0.0.0:8000`` from the root directory.
*Do not use this for deployment!*

In your browser, access ``http://127.0.0.1:8000/`` and continue from there.

### PyLint

To be able to run PyLint, go into content/static/yt_api.py, comment out the import from secret settings and set yt_api_key = "". Otherwise PyLint will not run because
it tries to import from a file that doesn't exist.

### Deployment Setup

This application can be deployed using a web server as any other Django application.
Remember to use a secret key that is not stored in any repository or similar, and disable DEBUG mode (``settings.py``).

**Step-by-Step Instructions**

1. Log into your system with a sudo user
1. Install system requirements
1. Create a folder, e.g. ``mkdir /srv/collab-coursebook/``
1. Change to the new directory ``cd /srv/collab-coursebook/``
1. Clone this repository ``git clone URL .``
1. Set up a virtual environment using the proper python version ``virtualenv venv -p python3``
1. Activate virtualenv ``source venv/bin/activate``
1. Update tools ``pip install --upgrade setuptools pip wheel``
1. Install python requirements ``pip install -r requirements.txt``
1. Install further python requirements ``pip install psycopg2-binary uwsgi``
1. Create postgres user and database and grant rights
   * sudo -u postgres createuser <username>
   * sudo -u postgres createdb <dbname>
   * sudo -u postgres psql 
   * psql=# alter user <username> with encrypted password '<password>'; 
   * psql=# grant all privileges on database <dbname> to <username> ;
1. Create the file ``collab_coursebook/settings_secrets.py`` (copy from ``settings_secrets.py.sample``) and fill it with the necessary secrets (e.g. generated by ``tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50``) (it is a good idea to restrict read permissions from others)
1. If necessary enable uwsgi proxy plugin for Apache e.g.``a2enmod proxy_uwsgi``
1. Edit the apache config to serve the application and the static and media files, e.g. on a dedicated system in ``/etc/apache2/sites-enabled/000-default.conf`` within the ``VirtualHost`` tag add:

    ```
    Alias /static /srv/collab-coursebook/static
    <Directory /srv/collab-coursebook/static>
      Require all granted
    </Directory>
   
    Alias /media /srv/collab-coursebook/media
    <Directory /srv/collab-coursebook/media>
      Require all granted
    </Directory>
       
    ProxyPassMatch ^/media/ !
    ProxyPassMatch ^/static/ !
    ProxyPass / uwsgi://127.0.0.1:3035/
    ```

or create a new config (.conf) file (similar to ``apache-collab-coursebook.conf``) replacing $SUBDOMAIN with the subdomain the system should be available under, and $MAILADDRESS with the e-mail address of your administrator and $PATHTO with the appropriate paths. Copy or symlink it to ``/etc/apache2/sites-available``. Then activate it with ``a2ensite collab-coursebook``.


1. Restart Apache ``sudo apachectl restart``
1. Create a dedicated user, e.g. ``adduser django --disabled-login``
1. Transfer ownership of the folder to the new user ``chown -R django:django /srv/collab-coursebook``
1. Copy or symlink the uwsgi config in ``uwsgi-collab-coursebook.ini`` to ``/etc/uwsgi/apps-available/`` and then symlink it to ``/etc/uwsgi/apps-enabled/`` using e.g., ``ln -s /srv/collab-coursebook/uwsgi-collab-coursebook.ini /etc/uwsgi/apps-available/collab-coursebook.ini`` **and** ``ln -s /etc/uwsgi/apps-available/collab-coursebook.ini /etc/uwsgi/apps-enabled/collab-coursebook.ini``
1. Test your uwsgi configuration file with``uwsgi --ini collab-coursebook.ini``
1. Restart uwsgi ``sudo systemctl restart uwsgi``
1. Execute the update script ``./utils/update.sh --prod``
1. If not already active on that server, obtain an SSL certificate, e.g., through [Let's Encrypt](https://certbot.eff.org/lets-encrypt/)

### Updates

To update the setup to the current version on the main branch of the repository use the update script ``utils/update.sh`` or ``utils/update.sh --prod`` in production.

Afterwards, you may check your setup by executing ``utils/check.sh`` or ``utils/check.sh --prod`` in production.


## Structure

This repository contains a Django project called collab_coursebook. The functionality is encapsulated into Django apps:

1. **base**: This app contains the general Django models used to represent courses, contents, etc.
1. **frontend**: This app provides everything the users see when reading or editing the content. It also contains a landing page.
1. **content**: This app provides models, rendering- and export code for the different supported types of contents.
1. **export**: This app contains export functions for the custom content collections (coursebooks).

## Developer Notes
* To regenerate translations use ````python manage.py makemessages -l de_DE --ignore venv````
* To create a data backup use ````python manage.py dumpdata --indent=2 > db.json --traceback````
