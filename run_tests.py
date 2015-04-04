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
    "SELECT count(*) FROM calls WHERE dest=172775430;",
    "SELECT count(*) FROM calls WHERE orig=196995859 AND duration > 300;",
    "SELECT orig, dest, ts, duration FROM calls WHERE orig=126818715 AND "
    "dest=174947999 AND duration > 2000;",
    "SELECT count(*) FROM calls WHERE ts BETWEEN '2015-01-08 00:00:00' AND "
    "'2015-01-08 23:59:59';",
    "SELECT count(*) FROM calls WHERE duration > 2000;",
    "SELECT count(*) FROM calls WHERE ts > '2015-04-02 09:59:59';"
)

mariaTimes = [0] * len(queries)
monetTimes = [0] * len(queries)


def time_query(db, query):
    cursor = db.cursor()
    start = time.time()
    cursor.execute(query)
    end = time.time()
    cursor.fetchall()
    cursor.close()
    return (end - start)

if __name__ == '__main__':
    numRuns = 10
    resultsFile = 'results.csv'

    for i in range(0, numRuns):
        print('[*] Run', i + 1, 'of', numRuns, file=sys.stderr)

        print('\t[*] (Re)starting VMs...', file=sys.stderr)
        subprocess.call(['./vm.sh', 'restart'], stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        print('\t[*] Running queries on MonetDB...', file=sys.stderr)
        monetCon = monetdb.sql.connect(username='monetdb', password='monetdb',
                                       database='adw', hostname='localhost',
                                       port=50000)

        for q in range(0, len(queries)):
            monetTimes[q] = monetTimes[q] + time_query(monetCon, queries[q])

        monetCon.close()

        print('\t[*] Running queries on MariaDB...', file=sys.stderr)
        mariaCon = mysql.connector.connect(user='root', password='',
                                           database='adw', host='localhost',
                                           port=33006)

        for q in range(0, len(queries)):
            mariaTimes[q] = mariaTimes[q] + time_query(mariaCon, queries[q])

        mariaCon.close()

    print('[!] Results saved as', resultsFile, file=sys.stderr)
    with open(resultsFile, 'w') as f:
        f.write('query,monetdb,mariadb\n')
        for i in range(0, len(queries)):
            f.write('"%s",%s,%s\n' % (queries[i],
                                      (monetTimes[i] / numRuns) * 100,
                                      (mariaTimes[i] / numRuns) * 100))
