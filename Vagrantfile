# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
  # Ensure noninteractive apt-get
  export DEBIAN_FRONTEND=noninteractive

  # Set time zone
  echo "Europe/Oslo" > /etc/timezone
  dpkg-reconfigure tzdata

  # Install packages
  apt-get -y update
  apt-get -y install git make python-pip python-dev libxml2-dev libxslt1-dev \
          python-software-properties

  # Install nodejs
  add-apt-repository -y ppa:chris-lea/node.js
  apt-get -y update
  apt-get -y install nodejs

  # Install npm packages
  npm install -g bower grunt-cli
  cd /vagrant && npm install

  # Install pip packages
  pip install --use-mirrors -r /vagrant/requirements.txt
  pip install --use-mirrors -r /vagrant/dev-requirements.txt
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "precise64-current"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network :forwarded_port, guest: 5000, host: 5000
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
  config.vm.provision :shell, :inline => $script
end
