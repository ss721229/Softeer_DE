#!/usr/bin/env python3

import sys

current_movie_id = None
current_count = 0
current_sum = 0.0

for line in sys.stdin:
    movie_id, score, count = line.strip().split("\t")
    score = float(score)
    count = int(count)

    if movie_id == current_movie_id:
        current_sum += score
        current_count += count
    else:
        if current_movie_id:
            avg = round(current_sum / current_count, 1)
            print(f"{current_movie_id}\t{avg}")
        current_movie_id = movie_id
        current_sum = score
        current_count = count

if current_movie_id:
    avg = round(current_sum / current_count, 1)
    print(f"{current_movie_id}\t{avg}")
