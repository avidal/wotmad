# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "wotmad.local"

  config.vm.box = "ubuntu/trusty64"

  config.vm.network "private_network", ip: "10.0.0.52"

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      apt-get update -qq
      apt-get install build-essential -qq --yes
      apt-get install postgresql postgresql-contrib -qq --yes
      apt-get install python-pip python-dev libpq-dev libevent-dev git -qq --yes
      pip install virtualenv virtualenvwrapper stevedore virtualenv-clone
      update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 LANGUAGE=en_US
      dpkg-reconfigure locales
    EOF
  end

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      cat > /tmp/create-db.sql <<EOD
        DROP DATABASE IF EXISTS wotmad;
        DROP ROLE IF EXISTS wotmad;
        CREATE ROLE wotmad WITH LOGIN PASSWORD 'wotmad';
        CREATE DATABASE wotmad WITH OWNER wotmad ENCODING 'utf8' LC_CTYPE 'en_US.utf8' LC_COLLATE 'en_US.utf8' template template0;
EOD

      su - postgres -c "psql template1 < /tmp/create-db.sql"
      rm /tmp/create-db.sql

      cat > /etc/postgresql/9.3/main/pg_hba.conf <<EOD
# TYPE  DATABASE    USER      ADDRESS       METHOD
local   all         postgres                peer
local   all         all                     md5

host    all         all       127.0.0.1/32  md5
EOD
    EOF
  end

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      if grep -q virtualenvwrapper /home/vagrant/.bashrc
      then
        echo "Already setup .bashrc"
      else
        cat >> /home/vagrant/.bashrc <<EOD
            export WORKON_HOME=/home/vagrant/.virtualenvs
            export PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache
            export PYTHONDONTWRITEBYTECODE=1

            source /usr/local/bin/virtualenvwrapper.sh

            workon wotmad
EOD
      fi

      if [ -f /vagrant/.env ]
      then
        echo "Already setup .env file."
      else
        cat >> /vagrant/.env <<EOD
DEBUG=1
DATABASE_URL=postgresql://wotmad:wotmad@/wotmad
SITE_URL=http://wotmad.local:5000
EOD
      fi

      cat > /tmp/setup-env.sh <<EOD
        mkdir -p /home/vagrant/.pip_download_cache
        virtualenv --no-site-packages /home/vagrant/.virtualenvs/wotmad
        echo /vagrant > /home/vagrant/.virtualenvs/wotmad/.project

        source /home/vagrant/.virtualenvs/wotmad/bin/activate
        cd /vagrant/
        PYTHONUNBUFFERED=1 PIP_DOWNLOAD_CACHE=/home/vagrant/.pip_download_cache pip install -r requirements.txt
EOD
      su - vagrant -c "/bin/bash /tmp/setup-env.sh"
      rm /tmp/setup-env.sh
    EOF
  end

end
