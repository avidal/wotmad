# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "wotmad.local"

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network "private_network", ip: "10.0.0.100"
  config.berkshelf.enabled = true

  config.vm.provision :shell do |sh|
    sh.inline = <<-EOF
      apt-get update -qq
      apt-get install ruby1.9.3 build-essential -qq --yes
      apt-get install python-pip python-dev libpq-dev libevent-dev -qq --yes
      gem install chef --version 11.4.4 --no-ri --no-rdoc
      pip install virtualenv virtualenvwrapper stevedore virtualenv-clone autoenv
      update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 LANGUAGE=en_US
      dpkg-reconfigure locales
    EOF
  end

  config.vm.provision :chef_solo do |chef|
    chef.json = {
      :postgresql => {
          :config => {
              :listen_addresses => 'localhost'
          },
          :password => {
              :postgres => '3175bce1d3201d16594cebf9d7eb3f9d'
          },
          :pg_hba => [
              {
                  :type => 'local',
                  :db => 'all',
                  :user => 'wotmad',
                  :addr => nil,
                  :method => 'md5'
              }
          ]
      }
    }

    chef.run_list = [
      "recipe[apt]",
      "recipe[build-essential]",
      "recipe[postgresql::server]",
      "recipe[postgresql::config_initdb]"
    ]

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
            source /usr/local/bin/activate.sh

            workon wotmad
EOD
      fi

      if [ -f /vagrant/.env ]
      then
        echo "Already setup .env file."
    else
        cat >> /vagrant/.env <<EOD
            DEBUG = True
            DATABASE_URL = postgresql://wotmad:wotmad@/wotmad
            SITE_URL=http://wotmad.local
EOD

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
