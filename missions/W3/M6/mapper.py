#!/usr/bin/env python3

import sys
import json

for line in sys.stdin:
    try:
        review = json.loads(line)
        asin = review.get("asin")
        score = review.get("rating")

        if asin and score is not None:
            print(f"{asin}\t{score}\t1")
    except json.JSONDecodeError:
        continue  # skip malformed lines