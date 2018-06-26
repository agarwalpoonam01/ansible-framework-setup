Ansible Framwork for Assessment App setup 
=========

This Ansible role is an attempt to solve these requirements:

- Pingtest to test the ansible setup is working.
- EnableLogin to allow deployment with ssh key instead of password.
- Security message before and after the login.
- Firewall rules to make server secure from network.
- To make sure user doesn't get timeout error additional service to handle the request along with redis-cache.
- Deploys the App with nginx as a web-server.
- Tried to install pyenv (install_virtual_env) but as this requires login and logout I used python virtualenv


Requirements
------------

* Ansible 2.3.1.0
* Python 2.7.10

Installation
-------------
- Python
```
$ sudo apt-get install -y gcc-multilib g++-multilib libffi-dev libffi6 libffi6-dbg python-crypto python-mox3 python-pil python-ply libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libgdbm-dev dpkg-dev quilt autotools-dev libreadline-dev libtinfo-dev libncursesw5-dev tk-dev blt-dev libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libsqlite3-dev libgpm2 mime-support netbase net-tools bzip2

$ wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
$ tar xvf Python-2.7.10.tgz
$ cd Python-2.7.10/

$ ./configure --prefix /usr/local/lib/python2.7.10 --enable-ipv6
$ make
$ sudo make install

$ /usr/local/lib/python2.7.10/bin/python -V
Python 2.7.10 
```

- PIP
```
$ apt-get update
$ apt-get -y install python-pip
```

- Ansible
```
$ pip install ansible
```

Deployment Steps
---------------

```
- Check the setup.
$ ansible-playbook -i hosts library/enable_login.yml 

- Copy id_rsa.pub key of the source machine to roles/eanble_login/files/authorized_keys
$ cat ~/.ssh/is_rsa.pu > roles/eanble_login/files/authorized_keys

- Enable the login by keeping the ssh public key in authorised_key file
$ ansible-playbook -i hosts library/enable_login.yml 

- Deploy the app.
$  ansible-playbook -i hosts library/deploy_app.yml
```

Dependencies
------------

none


Tested VM as the App server
---------------------------

A vagrant environment has been used to test the role. You nee to have virtualbox, vagrant and Add Vagrantfile in the repo to a directory of your choice.

```
$ sudo apt-get install virtualbox
$ sudo apt-get install vagrant
$ mkdir appserver
$ cd appserver
# Copy Vagrantfile to this location
$ vagrant up
```

Author Information
------------------

Poonam Agarwal (agrawal.poonam2015@gmail.com)

https://about.me/poonamagrawal