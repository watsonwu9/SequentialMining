#! /usr/bin/env python

"""
Usage:
    prefixspan.py (frequent | top-k | contiguous-frequent) <threshold>
"""

from __future__ import print_function

import sys
from collections import defaultdict
from heapq import heappop, heappush

from docopt import docopt

results = []

def contiguous_frequent(patt, mdb):
    print ("now we are going to scan the database")
    occurs = defaultdict(list)
    for (i, startpos) in mdb:

        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            l.append((i, j + 1))    

    for (c, newmdb) in occurs.iteritems():
        if len(newmdb) >= minsup:
            frequent(patt + [c], newmdb)

def frequent(patt, mdb):
    results.append((mdb, patt))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        if startpos < len(seq):
            l = occurs[seq[startpos]]
            l.append((i, startpos + 1))
      
    for (c, newmdb) in occurs.iteritems():
        if len(newmdb) >= minsup:
            frequent(patt + [c], newmdb)

def calculate_frequent(mdb):
    num_seq = []
    for(seq_index,j) in mdb:
        num_seq.append(seq_index)
    return len(set(num_seq))

def sequence_format(patt):
    pattern = ''
    for element in patt:
        pattern =pattern + element + ';'
    return pattern.strip(';')

def frequent_rec(patt, mdb):
    results.append((len(mdb), patt))
    occurs = defaultdict(list)

    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))
     
    for (c, newmdb) in occurs.iteritems():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)


def topk_rec(patt, mdb):
    heappush(results, (len(mdb), patt))
    if len(results) > k:
        heappop(results)

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for (c, newmdb) in sorted(occurs.iteritems(), key=(lambda (c, newmdb): len(newmdb)), reverse=True):
        if len(results) == k and len(newmdb) <= results[0][0]:
            break
        topk_rec(patt + [c], newmdb)



if __name__ == "__main__":
    argv = docopt(__doc__)

    db = []
    f = open("review.txt",'r')
    for line in f.readlines():
        line = line.strip()
        words = line.split(' ')
        db.append(words)
    f.close()

    if argv["frequent"]:
        minsup = int(argv["<threshold>"])
        f = frequent_rec

    elif argv["top-k"]:
        k = int(argv["<threshold>"])
        f = topk_rec

    elif argv['contiguous-frequent']:
        minsup = int(argv["<threshold>"])
        f = contiguous_frequent


    f([], [(i, 0) for i in xrange(len(db))])
    output_file = open("parking.txt",'a+')
    if argv["top-k"]:
        results.sort(key=(lambda (freq, patt): (-freq, patt)))
    for (freq, patt) in results:
        print("{}: {}".format(patt, freq))
        num_freq = calculate_frequent(freq)
        if num_freq >= minsup:
            output_file.write("%d:%s\n"%(num_freq,sequence_format(patt)))
    output_file.close()






