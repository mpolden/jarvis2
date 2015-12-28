# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  # Versions later than 8.2.1 don't have VirtualBox guest additions
  # preinstalled, so synced_folder defaults to rsync
  config.vm.box_version = "8.2.1"
  config.vm.synced_folder ".", "/vagrant"
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
  config.vm.define "dev", primary: true do |dev|
    # Flask port
    config.vm.network :forwarded_port, guest: 5000, host: 5000
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
    end
  end
  config.vm.define "prod", autostart: false do |prod|
    # nginx port
    config.vm.network :forwarded_port, guest: 80, host: 8080
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
    end
  end
end
