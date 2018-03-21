#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install curl git wget -y
sudo apt-get install python3-pip bluetooth libbluetooth-dev libusb-dev eclipse eclipse-jdt -y
sudo apt-get install lib32ncurses5 lib32z1 y
sudo apt-get install libxrender1:i386 libxtst6:i386 libxi6:i386 libxrender1 libxtst6 libxi6 libxext-dev -y
pip3 install --upgrade pip

BASE_URL_8=http://download.oracle.com/otn-pub/java/jdk/8u161-b12/2f38c3b165be4555a1fa6e98c45e0808/jdk-8u161-linux-x64.tar.gz

curl -C - -LR#OH "Cookie: oraclelicense=accept-securebackup-cookie" -k "${BASE_URL_8}"

sudo mkdir /usr/local/java/
sudo tar zxvf jdk-8u161-linux-x64.tar.gz
sudo mv jdk1.8.0_161 /usr/local/java/jdk1.8.0

export JAVA_HOME=/usr/local/java/jdk1.8.0
export JVM_HOME=/usr/local/java/jdk1.8

echo "export JAVA_HOME=/usr/local/java/jdk1.8.0" >> ~/.bashrc
echo "export JVM_HOME=/usr/local/java/jdk1.8.0" >> ~/.bashrc

# install vim and configure it
# sudo apt install vim
# touch ~/.vimrc
# dd of=~/.vimrc << EOF
# set nu
# syntax on
# set tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab
# EOF

sudo dd of=/etc/udev/rules.d/70-lego.rules << EOF
# Lego NXT brick in normal mode
SUBSYSTEM=="usb", DRIVER=="usb", ATTRS{idVendor}=="0694", ATTRS{idProduct}=="0002", GROUP="lego-usb", MODE="0660"
# Lego NXT brick in firmware update mode (Atmel SAM-BA mode)
SUBSYSTEM=="usb", DRIVER=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="6124", GROUP="lego-usb", MODE="0660"
EOF
sudo groupadd lego-usb
sudo gpasswd -a lego lego-usb
sudo gpasswd -a root lego-usb
sudo udevadm control --reload-rules 

wget http://ufpr.dl.sourceforge.net/project/nxt.lejos.p/0.9.1beta-3/leJOS_NXJ_0.9.1beta-3.tar.gz
tar -xzvf leJOS_NXJ_0.9.1beta-3.tar.gz
mv ./leJOS_NXJ_0.9.1beta-3 /opt/lejos
rm -rf ./leJOS*

echo "export LEJOS_HOME=/opt/lejos" >> ~/.bashrc
echo "export NXT_HOME=/opt/lejos" >> ~/.bashrc
echo "export PATH=\$PATH:\$LEJOS_HOME/bin" >> ~/.bashrc
echo "export LEJOS_NXT_JAVA_HOME=/usr/local/java/jdk1.8.0" >> ~/.bashrc

cd /opt/lejos/build/ && ant
