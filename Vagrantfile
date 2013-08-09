# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
  # Ensure noninteractive apt-get
  export DEBIAN_FRONTEND=noninteractive

  # Set time zone
  echo "Europe/Oslo" > /etc/timezone
  dpkg-reconfigure tzdata

  # Install packages
  add-apt-repository -y ppa:chris-lea/node.js
  apt-get -y --quiet update
  apt-get -y --quiet install git make python-pip python-dev libxml2-dev \
          libxslt1-dev nodejs zlib1g-dev

  # Install npm packages
  npm install --silent -g bower grunt-cli
  cd /vagrant && npm install --silent

  # Install pip packages
  pip install --quiet --use-mirrors --upgrade -r /vagrant/requirements.txt \
          -r /vagrant/dev-requirements.txt
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "raring64-current"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/raring/current/raring-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network :forwarded_port, guest: 5000, host: 5000
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
  config.vm.provision :shell, :inline => $script
end
