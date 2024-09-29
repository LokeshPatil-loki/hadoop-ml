# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  config.vm.box = "boxomatic/centos-stream-9"

  config.vm.network "private_network", ip: "192.168.56.102"

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true
  
    # Customize the amount of memory on the VM:
    vb.memory = "4096"
    vb.cpus = 2
  end
  config.vm.provision "shell", inline: <<-SHELL
    sudo yum update
    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    sudo systemctl start docker
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    sudo yum install git -y
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
  SHELL
end
