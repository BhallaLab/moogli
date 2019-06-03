#!/usr/bin/env bash

apt-get install -y libopenscenegraph-dev
apt-get install -y libqt5-dev
apt-get install -y libqt5-opengl-dev
apt-get install -y python3-sip-dev
apt-get install -y python3-numpy
apt-get install -y python3-matplotlib cmake g++
python3 -m pip install pymoose 
python3 -m pip install numpy --upgrade 

