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

numNumbers = 500
minCalls = 400
maxCalls = 1200
minDuration = 15  # Seconds
maxDuration = 1*60*60  # Seconds

if __name__ == "__main__":
    numbers = []
    calls = []
    endDate = date.today()
    initDate = endDate - timedelta(days=120)

    # Generate list of random phone numbers
    while len(numbers) < numNumbers:
        tlf = random.randrange(600000000, 699999999)
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

    for l in calls:
        print("%s,%s,%s,%s" % l)
