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
      gem install chef --version 11.4.4 --no-ri --no-rdoc
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

end
