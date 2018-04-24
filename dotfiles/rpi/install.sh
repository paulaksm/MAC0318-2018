sudo apt-get update
sudo apt-get upgrade

# Raspberry config
sudo apt-get remove --purge libreoffice*
sudo apt-get purge minecraft-pi
sudo apt-get purge wolfram-engine

# Installing opencv-3.3.0 on python3
sudo apt-get install build-essential git cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install libgtk2.0-dev 
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libatlas-base-dev gfortran imagemagick
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
    -D WITH_GTK=ON \
    -D WITH_JPEG=OFF ..
make -j3
sudo make install
sudo ldconfig

# Installing libraries for nxt robot
sudo pip3 install keyboard
sudo pip3 install pybluez
sudo pip3 install pyusb
sudo apt-get install bluetooth libbluetooth-dev
sudo apt-get install libusb-dev

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

# Install remaining python packages
sudo pip3 install -r requirements.txt

# Remember to enable SSH and set timezone and keyboard settings 
# Expand rootfs if not done automatically wheh booting for the first time
