"""
- main data type: fixed-size array
- no explicit iteration
- computation unfolds as search, selection, and transformation
"""

import sys
import numpy as np

characters = np.array([' ']+list(open(sys.argv[1]).read())+[' '])
characters[~np.char.isalpha(characters)] = ' '
characters = np.char.lower(characters)
sp = np.where(characters == ' ')
# trick: double the indexes and take pairs
sp2 = np.repeat(sp, 2)
# e.g. [0,0,5,5,9,9,11,11,0,0]
w_ranges = np.reshape(sp2[1:-1], (-1, 2))
# -1: take all data, 2: num of elements in 2nd dimension
# so it'll be [0,5],[5,9]...[11,0]
# only take ranges where diff is larger than 2
w_ranges = w_ranges[np.where(w_ranges[:, 1] - w_ranges[:, 0] > 2)]
words = list(map(lambda r: characters[r[0]:r[1]], w_ranges))
s_words = np.array(list(map(lambda w: ''.join(w).strip(), words)))
stop_words = np.array(list(set(open('./files/stop_words.txt', 'r').read().split(','))))
ns_words = s_words[~np.isin(s_words, stop_words)]
uniq, counts = np.unique(ns_words, axis=0, return_counts=True)
wf_sorted = sorted(zip(uniq, counts), key=lambda t: t[1], reverse=True)

for w, c in wf_sorted[:25]:
    print(f'{w}-{c}')