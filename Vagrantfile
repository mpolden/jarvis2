# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version ">= 1.8"

Vagrant.configure("2") do |config|
  config.vm.box = "bento/debian-8.7"
  config.vm.synced_folder ".", "/vagrant"
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |v|
    v.memory = 1024
    v.cpus = 2
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
