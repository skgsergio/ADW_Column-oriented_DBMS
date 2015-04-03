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
mariadb_repo="deb http://mirror2.hs-esslingen.de/mariadb/repo/10.0/ubuntu trusty main"
mariadb_key="--recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db"

# Functions
status() { echo -e "\e[1;34m>>> $@\e[0m"; }

# Do things... stuff...
status "Updating APT..."
sudo apt-get update

status "Installing utils..."
sudo apt-get install -y software-properties-common htop

status "Adding MariaDB repo..."
sudo apt-key adv $mariadb_key
sudo add-apt-repository -y "$mariadb_repo"

status "Updating APT..."
sudo apt-get update

status "Installing MariaDB..."
DEBIAN_FRONTEND=noninteractive sudo -E apt-get install -y mariadb-server

status "Creating database in MariaDB..."
mysql -u root <<EOF
CREATE DATABASE adw;
EOF
if [[ $? == 0 ]]; then echo "database created successfully."; fi

status "Importing data into MariaDB (this may take a while)..."
bzcat /DB/test_db.sql.bz2 | time mysql -u root adw > /dev/null
if [[ $? == 0 ]]; then echo "data imported successfully."; fi
