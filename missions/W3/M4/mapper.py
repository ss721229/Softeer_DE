#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    if row[0] == "0":
        print(f"negative\t1")
    elif row[0] == "4":
        print(f"positive\t1")
    elif row[0] == "2":
        print(f"neutral\t1")