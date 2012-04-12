Installation Guide
==================

The following is an installation on how to set up and deploy the
Candidates Emailer web application.

AWS EC2 Instance Setup
----------------------

A micro or small instance is suitable for install this
application. Remember to place the instance in a security group with
HTTP and HTTPS (port 80 and port 443) open.


Prerequisites
-------------

Assuming that the operating system is Linux and the distribution is
Ubuntu 10.04 LTS, the following line must be added the apt.sources
file.

Append these lines to: `/etc/apt/sources.list`

> deb http://nginx.org/packages/ubuntu/ lucid nginx
> deb-src http://nginx.org/packages/ubuntu/ lucid nginx

Then install the following Debian/Ubuntu packages:

> sudo apt-get update
> sudo apt-get install nginx python-dev libxml2-dev python-setuptools
> build-essential git-core

Install the `pip` Python package manager:

> sudo easy_install pip


Installing virtualenv & virtualenvwrapper
-----------------------------------------

To set up a virtualenv to host the application, install the virtualenv
and virtualenvwrapper package:

> sudo pip install virtualenv virtualenvwrapper

Add the following lines to the user's `bashrc` file:

> echo "export WORKON_HOME='~/.virtualenvs' >> ~/.bashrc
> echo "source virtualenvwrapper.sh" >> ~/.bashrc


Creating the `odesk` virtualenv
-------------------------------

If using the configuration provided in the `deploy/uwsgi.ini`
configuration, then create the following virtualenv, as non-root:

> mkvirtualenv odesk


Clone and setup the Candidates Emailer app
------------------------------------------

In your `HOME` directory clone the Candidates Emailer app:

> git clone git://github.com/mkhattab/candidates_emailer.git


Make sure you have activated the `odesk` virtualenv and run the
following commands:

> workon odesk
> cd ~/candidates_emailer
> pip install -r requirements.txt


The above commands should install the required packages for the
project to run.


Configure Nginx and uWSGI
-------------------------

Finally, last step so far. Configure uWSGI using this Upstart
script. Of course, if you're deploying to a different server with
different paths, make sure the paths in `deploy/uwsgi.ini` and
`project/wsgi.py` are correct.


Create and append the following file in: `/etc/init/uwsgi.conf`

> # file: /etc/init/uwsgi.conf
> description "uWSGI starter"
> 
> start on (local-filesystems and runlevel [2345])
> stop on runlevel [016]
> 
> respawn
> 
> # home - is the path to our virtualenv directory
> # pythonpath - the path to our django application
> # module - the wsgi handler python script
> 
> exec /home/ubuntu/.virtualenvs/odesk/bin/uwsgi \
> --uid ubuntu \
> --gid ubuntu \
> --ini /home/ubuntu/candidates_emailer/deploy/uwsgi.ini

Change the following lines in the Nginx conf:
`/etc/nginx/conf.d/default.conf`

From:

>     location / {
>         root   /usr/share/nginx/html;
>         index  index.html index.htm;
>     }


To:

>     location / {
>         uwsgi_pass 127.0.0.1:3031;
>         include uwsgi_params;
>     }


If you've reach this line, then you've made it hopefully. Lastly,
start the uWSGI and restart Nginx service:

sudo start uwsgi
sudo /etc/init.d/nginx restart


