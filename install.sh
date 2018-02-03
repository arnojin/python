#!/bin/bash
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar -xvzf Python-3.6.4.tgz
cd Python-3.6.4/
./configure
make && make install
ln -s /usr/local/bin/python3.6 /usr/bin/python3
python3 -V