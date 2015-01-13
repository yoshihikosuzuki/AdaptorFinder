#!/usr/bin/env python
#coding: utf-8

from pbcore.io import FastaReader
from multiprocessing import Pool
import sys

K = 14

RC_MAP = dict( zip("ACGTacgtNn-", "TGCAtgcaNn-") )


def find_candidate(subread):

    forward = subread.sequence
    revcomp = "".join([RC_MAP[c] for c in forward[::-1]])
    alist = sorted({forward[i:i+K]:i for i in range(len(forward) - K)}.items())
    blist = sorted({revcomp[i:i+K]:i for i in range(len(revcomp) - K)}.items())
    
    mlist = []
    i = j = 0
    while i < len(alist) and j < len(blist):
        if alist[i][0] == blist[j][0]:
            mlist.append(alist[i][1])
            i += 1
            j += 1
        elif alist[i][0] <= blist[j][0]:
            i += 1
        else:
            j += 1
        
    mlist = sorted(mlist)
    length = 0
    for i in range(len(mlist)):
        if i == 0 or mlist[i - 1] + K <= mlist[i]:
            length += K
        else:
            length += mlist[i] - mlist[i - 1]
        
    return subread.name, length


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="find candidates of subreads adaptor unremoved")
    parser.add_argument('fasta_file', help="a file that contains the subread information")
    parser.add_argument('--n_core', type=int, default=12, help="number of processes")
    parser.add_argument('--len_th', type=int, default=1, help="length threshold of k-mer matching region")
    args = parser.parse_args()
    exe_pool = Pool(args.n_core)

    fasta_file = args.fasta_file
    length_threshold = args.len_th

    subreads = FastaReader(fasta_file)
    candidate = []
    for res in exe_pool.imap(find_candidate, subreads):
        if res[1] > length_threshold:
            print res[0], res[1]
