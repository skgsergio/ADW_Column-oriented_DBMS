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
monetdb_repo="deb http://dev.monetdb.org/downloads/deb/ trusty monetdb"
monetdb_key="--fetch-keys http://dev.monetdb.org/downloads/MonetDB-GPG-KEY"

# Functions
status() { echo -e "\e[1;34m$@\e[0m"; }

# Do things... stuff...
status ">>> Updating APT..."
sudo apt-get update

status ">>> Installing utils..."
sudo apt-get install -y software-properties-common htop

status ">>> Adding MonetDB repo..."
sudo apt-key adv $monetdb_key
sudo add-apt-repository -y "$monetdb_repo"

status ">>> Updating APT..."
sudo apt-get update

status ">>> Installing MonetDB..."
sudo apt-get install -y monetdb5-sql monetdb-client

status ">>> Enabling & starting MonetDB..."
sudo sed -i 's/STARTUP="no"/STARTUP="yes"/' /etc/default/monetdb5-sql
sudo service monetdb5-sql start

status ">>> Creating database in MonetDB..."
sudo -u monetdb monetdb create adw
sudo -u monetdb monetdb release adw

status ">>> Importing data into MonetDB (this may take a while)..."
cat > $HOME/.monetdb <<EOF
user=monetdb
password=monetdb
EOF
bzcat /DB/test_db.sql.bz2 | mclient -d adw > /dev/null
if [[ $? == 0 ]]; then echo "data imported successfully."; fi
