#!/bin/zsh

pip install -e .
sudo -H mkdir /mnt/shared
sudo -H chown $USERNAME /mnt/shared
cd benchmarks/ssn
./gen.sh 10000
cd ../..

echo "Please update /etc/hosts now..."
