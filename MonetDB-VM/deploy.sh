#!/bin/bash
#
# Copyright (C) 2015 Sergio Conde Gomez, Cristina Hermoso Garcia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# Variables
monetdb_mirror="http://dev.monetdb.org/downloads/deb/"
monetdb_distro="trusty"
monetdb_key="http://dev.monetdb.org/downloads/MonetDB-GPG-KEY"

# Functions
status() { echo -e "\e[1;34m$@\e[0m"; }

# Do things... stuff...
status ">>> Updating APT..."
sudo apt-get update

status ">>> Installing utils..."
sudo apt-get install -y software-properties-common htop

status ">>> Adding MonetDB repo..."
sudo apt-key adv --fetch-keys $monetdb_key
sudo add-apt-repository -y "deb $monetdb_mirror $monetdb_distro monetdb"

status ">>> Updating APT..."
sudo apt-get update

status ">>> Installing MonetDB..."
sudo apt-get install -y monetdb5-sql monetdb-client

status ">>> Enabling MonetDB..."
sudo sed -i 's/STARTUP="no"/STARTUP="yes"/' /etc/default/monetdb5-sql

status ">>> Starting MonetDB..."
sudo service monetdb5-sql start

status ">>> Loading database in MonetDB..."
# TBD