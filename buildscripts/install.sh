#!/bin/bash

python -c 'import sys; print sys.path'
sudo apt-add-repository ppa:mantid/mantid -y && sudo apt-get update -q
# Download deb file from sourceforge as it's far quicker that the ISIS repo
sudo apt-get install gdebi -y
export mantiddeb=$(curl -sL https://github.com/mantidproject/download.mantidproject.org/raw/master/releases/nightly.txt | grep trusty)
wget http://downloads.sourceforge.net/project/mantid/Nightly/$mantiddeb -O /tmp/mtn.deb
sudo gdebi --option=APT::Get::force-yes=1,APT::Get::Assume-Yes=1 -n /tmp/mtn.deb
mkdir $HOME/.mantid && echo -e "UpdateInstrumentDefinitions.OnStartup=0\nCheckMantidVersion.OnStartup=0\n" > $HOME/.mantid/Mantid.user.properties
# Circumvent a bug in mantid when instrument updates are unavilable. Fixed on 17/08/2017
mkdir $HOME/.mantid/instrument
pip install -r setup-requirements.txt -r install-requirements.txt -r test-requirements.txt coveralls

