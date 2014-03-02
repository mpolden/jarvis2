# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64-current"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.synced_folder ".", "/vagrant", nfs: true
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
  config.vm.define "dev", primary: true do |dev|
    config.vm.network "private_network", ip: "172.16.1.10"
    # Flask port
    config.vm.network :forwarded_port, guest: 5000, host: 5000
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
      ansible.inventory_path = "provisioning/development"
    end
  end
  config.vm.define "prod" do |prod|
    config.vm.network "private_network", ip: "172.16.1.11"
    # nginx port
    config.vm.network :forwarded_port, guest: 80, host: 8080
    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "provisioning/playbook.yml"
      ansible.inventory_path = "provisioning/production"
    end
  end
end
