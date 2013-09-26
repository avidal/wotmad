#!/bin/bash

# Script to set up a Django project on Vagrant.

# Installation settings

PROJECT_NAME=$1

DB_NAME=$PROJECT_NAME
VIRTUALENV_NAME=$PROJECT_NAME

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

# Python development packages
PACKAGES="build-essential python python-dev python-distribute python-pip git mercurial"

# Postgres
PACKAGES="$PACKAGES libpq-dev postgresql-9.1"

# gevent (from chaussette)
PACKAGES="$PACKAGES libevent-dev"

# node.js (for .less compilation)
PACKAGES="$PACKAGES nodejs"

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Update the apt cache
apt-get update -qq -y

# Add the chris lea node.js ppa
echo "Adding chris-lea node.js ppa."
apt-get install -qq -y python-software-properties
add-apt-repository -y ppa:chris-lea/node.js > /dev/null 2>&1

# Update the apt cache again. This is necessary to install nodejs later.
# The reason we have to do it twice is that without doing it the first
# time we can't install python-software-properties.
echo "Updating apt-cache."
apt-get update -qq -y

echo "Installing required system packages."
apt-get install -qq -y $PACKAGES

# Set python to unbuffered so it doesn't look like some of the below stuff is hanging
export PYTHONUNBUFFERED=1

# virtualenv global setup
echo "Installing system python packages (virtualenv et al)"
pip install -q virtualenv virtualenvwrapper stevedore virtualenv-clone

# bash environment global setup
cp -p $PROJECT_DIR/vagrant/bashrc /home/vagrant/.bashrc
su - vagrant -c "mkdir -p /home/vagrant/.pip_download_cache"

# ---

echo "Creating virtual environment."
su - vagrant -c "/usr/local/bin/virtualenv -q $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"

echo "Installing packages."
su - vagrant -c "source $VIRTUALENV_DIR/bin/activate && \
    cd $PROJECT_DIR && \
    PYTHONUNBUFFERED=1 PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache pip install -r requirements.txt"

# add in ipython
su - vagrant -c "$VIRTUALENV_DIR/bin/pip install -q ipython"

echo "workon $VIRTUALENV_NAME" >> /home/vagrant/.bashrc

# Run the database setup script as the postgres user
sudo su postgres -c "psql template1 -f $PROJECT_DIR/vagrant/database.sql"

# Copy the pg_hba.conf
cp -p $PROJECT_DIR/vagrant/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf
chown postgres:postgres /etc/postgresql/9.1/main/pg_hba.conf

# And reload postgres
/etc/init.d/postgresql reload

# First, make sure that manage.py is executable
chmod +x $PROJECT_DIR/manage.py

echo "Synchronizing database."
# Synchronize the database by reading in the production database dump
su - vagrant -c "source $VIRTUALENV_DIR/bin/activate && \
    cd $PROJECT_DIR && \
    PYTHONUNBUFFERED=1 ./manage.py syncdb --noinput"


echo "Migrating..."
su - vagrant -c "source $VIRTUALENV_DIR/bin/activate && \
    cd $PROJECT_DIR && \
    PYTHONUNBUFFERED=1 ./manage.py migrate"

# Get our global node.js dependencies
echo "Installing node.js dependencies."
npm install -g -q grunt-cli > /dev/null

# Now install the node.js deps for the project
su - vagrant -c "cd $PROJECT_DIR && npm install -q grunt grunt-contrib-less grunt-contrib-watch > /dev/null"

echo "Done."
