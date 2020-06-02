Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
  end
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update -y
    apt-get upgrade -y
    apt-get dist-upgrade -y
    apt-get install -y python3-dev python3-wheel python3-setuptools python3-six python3-pip
    pip3 install virtualenv
    pip3 install virtualenvwrapper
    apt-get autoremove -y
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
  SHELL
end