# Raspberry config
sudo apt-get -y  remove --purge libreoffice*
sudo apt-get -y purge minecraft-pi
sudo apt-get -y purge wolfram-engine

# Installing opencv-3.3.0 on python3
sudo apt-get -y install build-essential git cmake pkg-config
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get -y install libgtk2.0-dev libgtk-3-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libgtk2.0-dev
sudo apt-get -y install libatlas-base-dev gfortran
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib.zip
cd ~/opencv-3.3.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D BUILD_EXAMPLES=ON \
    -D WITH_JPEG=OFF ..
make -j2
sudo make install
sudo ldconfig

# Installing libraries for nxt robot
sudo pip3 install keyboard
sudo pip3 install pybluez
sudo pip3 install pyusb
sudo apt-get -y install bluetooth libbluetooth-dev
sudo apt-get -y  install libusb-dev

# Setup USB connection for nxt robot
sudo dd of=/etc/udev/rules.d/70-lego.rules << EOF
# Lego NXT brick in normal mode
SUBSYSTEM=="usb", DRIVER=="usb", ATTRS{idVendor}=="0694", ATTRS{idProduct}=="0002", GROUP="lego", MODE="0660"
# Lego NXT brick in firmware update mode (Atmel SAM-BA mode)
SUBSYSTEM=="usb", DRIVER=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="6124", GROUP="lego", MODE="0660"
EOF
sudo groupadd lego
sudo gpasswd -a pi lego
sudo gpasswd -a root lego
sudo udevadm control --reload-rules

# vim configuration file
dd of=~/.vimrc << EOF
set nu
syntax on
set tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab
EOF

