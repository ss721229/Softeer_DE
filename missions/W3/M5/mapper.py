#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)
next(reader)

for row in reader:
    print(f'{row[1]}\t{row[2]}\t1')    