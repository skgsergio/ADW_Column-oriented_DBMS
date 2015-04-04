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

import random
from datetime import datetime, date, time, timedelta

days = 240
numNumbers = 800
minCalls = 1125
maxCalls = 2750
minDuration = 15  # Seconds
maxDuration = 1*60*60  # Seconds

if __name__ == "__main__":
    numbers = []
    calls = []
    endDate = date.today()
    initDate = endDate - timedelta(days=days)

    # Generate list of random phone numbers
    while len(numbers) < numNumbers:
        tlf = random.randrange(100000000, 199999999)
        if tlf not in numbers:
            numbers.append(tlf)

    # Generate list of random calls
    for origNumber in numbers:
        for i in range(random.randrange(minCalls, maxCalls)):
            destNumber = random.choice(numbers)
            while destNumber == origNumber:
                destNumber = random.choice(numbers)

            duration = random.randrange(minDuration, maxDuration)
            callDate = initDate + (endDate - initDate) * random.random()
            callTime = time(int(23 * random.betavariate(8, 3)),
                            int(59 * random.random()),
                            int(59 * random.random()))

            calls.append((origNumber,
                          destNumber,
                          datetime.combine(callDate, callTime),
                          duration))

    calls.sort(key=lambda i: i[2])  # Order by date

    with open('generated_nums.txt', 'w') as f:
        for n in numbers:
            f.write("%s\n" % n)

    with open('test_db.sql', 'w') as f:
        f.write("""/* Table creation */
CREATE TABLE calls (
  id INT NOT NULL AUTO_INCREMENT,
  orig VARCHAR(9) NOT NULL,
  dest VARCHAR(9) NOT NULL,
  ts TIMESTAMP NOT NULL,
  duration INT NOT NULL,
  PRIMARY KEY (id)
);
/* Data import */
""")

        i = 0
        for l in calls:
            i = i + 1
            f.write("INSERT INTO calls VALUES ('%s','%s','%s','%s','%s');\n"
                    % (i, l[0], l[1], l[2], l[3]))
