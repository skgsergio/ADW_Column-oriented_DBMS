#!/usr/bin/env python
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

import sys
import time
import subprocess
import monetdb.sql
import mysql.connector

queries = (
    "SELECT count(*) FROM calls WHERE dest=167429847;",
    "SELECT count(*) FROM calls WHERE duration > 2000;",
    "SELECT count(*) FROM calls WHERE ts > '2015-04-02 09:59:59';",
    "SELECT count(*) FROM calls WHERE ts BETWEEN '2015-01-08 00:00:00' "
    "AND '2015-01-08 23:59:59';",
    "SELECT count(*) FROM calls WHERE orig=106381066 AND duration > 300;",
    "SELECT orig, dest, ts, duration FROM calls WHERE dest=171480946;",
    "SELECT orig, dest, ts, duration FROM calls WHERE orig=101552551 "
    "AND dest=150982696;",
    "SELECT count(*) FROM calls WHERE orig=112979361 "
    "AND dest=104245541 AND duration > 2000;",
)

mariaTimes = [0] * len(queries)
monetTimes = [0] * len(queries)


def mariadb_query(query):
    mariaCon = mysql.connector.connect(user='root', password='',
                                       database='adw', host='localhost',
                                       port=33006)
    cursor = mariaCon.cursor()
    start = time.time()
    cursor.execute(query)
    end = time.time()
    mariaCon.close()
    return (end - start)


def monetdb_query(query):
    monetCon = monetdb.sql.connect(username='monetdb', password='monetdb',
                                   database='adw', hostname='localhost',
                                   port=50000)
    cursor = monetCon.cursor()
    start = time.time()
    cursor.execute(query)
    end = time.time()
    monetCon.close()
    return (end - start)

if __name__ == '__main__':
    numRuns = 10
    resultsFile = 'results.csv'

    for i in range(0, numRuns):
        print('[*] Run', i + 1, 'of', numRuns, file=sys.stderr)

        print('\t[*] Restarting VMs...', file=sys.stderr)
        subprocess.call(['./vm.sh', 'restart'], stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        print('\t[*] Running queries on MonetDB...', file=sys.stderr)

        for q in range(0, len(queries)):
            monetTimes[q] = monetTimes[q] + monetdb_query(queries[q])

        print('\t[*] Running queries on MariaDB...', file=sys.stderr)

        for q in range(0, len(queries)):
            mariaTimes[q] = mariaTimes[q] + mariadb_query(queries[q])

    print('[!] Results saved as', resultsFile, file=sys.stderr)
    with open(resultsFile, 'w') as f:
        f.write('query,monetdb,mariadb\n')
        for i in range(0, len(queries)):
            f.write('"%s",%s,%s\n' % (queries[i],
                                      (monetTimes[i] / numRuns) * 100,
                                      (mariaTimes[i] / numRuns) * 100))
