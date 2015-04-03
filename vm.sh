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

status() { echo -e "\e[1;34m>>> $@\e[0m"; }
exec_dir=$PWD

case "$1" in
    start|up)
        status "Starting MariaDB VM..."
        cd $exec_dir/MariaDB-VM
        vagrant up

        status "Starting MonetDB VM..."
        cd $exec_dir/MonetDB-VM
        vagrant up
        ;;
    stop|halt)
        status "Stopping MariaDB VM..."
        cd $exec_dir/MariaDB-VM
        vagrant halt

        status "Stopping MonetDB VM..."
        cd $exec_dir/MonetDB-VM
        vagrant halt
        ;;
    destroy)
        status "Destroying MariaDB VM..."
        cd $exec_dir/MariaDB-VM
        vagrant destroy

        status "Destroying MonetDB VM..."
        cd $exec_dir/MonetDB-VM
        vagrant destroy
        ;;
    status)
        vagrant global-status | grep $exec_dir | grep --color=none -E "(MonetDB-VM|MariaDB-VM)"
        ;;
    *)
        echo "Usage: $0 {start|stop|destroy|status}" 1>&2
        ;;
esac
