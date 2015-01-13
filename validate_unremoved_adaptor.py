#!/usr/bin/env python
#coding: utf-8

from pbcore.io import FastaReader
from multiprocessing import Pool
import sys
import os
import commands
import re

K = 14
RC_MAP = dict(zip("ACGT", "TGCA"))


def output_fasta(name, seq):
    with open(name, 'w') as f:
        f.write(">" + name + "\n" + seq)


def extract_alignment_info(s):
    check = re.search(r'\((\d+) nt\)', s)
    if check is None:
        return (0, 0.0, 0, 0, 0, 0, 0)
    else:
        return (int(check.groups()[0]),
                float(re.search(r'\n(.*?)%', s).groups()[0]),
                int(re.search(r'in (\d+) nt overlap', s).groups()[0]),
                int(re.search(r'\((\d+)-\d+:\d+-\d+\)', s).groups()[0]),
                int(re.search(r'\(\d+-(\d+):\d+-\d+\)', s).groups()[0]),
                int(re.search(r'\(\d+-\d+:(\d+)-\d+\)', s).groups()[0]),
                int(re.search(r'\(\d+-\d+:\d+-(\d+)\)', s).groups()[0]))


def validate_candidate(candidate):
    
    header, match_length, forward, lalign = candidate
    revcomp = "".join([RC_MAP[c] for c in forward[::-1]])

    pid = os.getpid()
    f_name = "tmp.f." + str(pid)
    r_name = "tmp.r." + str(pid)
    output_fasta(f_name, forward)
    output_fasta(r_name, revcomp)

    read_len, identity, ovlp_len, fstart, fend, rstart, rend = extract_alignment_info(commands.getoutput(lalign + " -3K1 -f -4 -g -4 " + f_name + " " + r_name))
    return header, match_length, read_len, identity, ovlp_len, fstart, fend, rstart, rend


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="validate the candidates and get alignments between the plus strand and the minus strand")
    parser.add_argument('candidate_file', help="a file that lists candidates of adaptor unremoved subreads")
    parser.add_argument('fasta_file', help="a file that contains the subread information")
    parser.add_argument('--lalign', type=str, default="/work2/yoshihiko_s/metaFALCON/etc/lalign36", help="the directory of lalign")
    parser.add_argument('--n_core', type=int, default=12, help="number of processes")
    parser.add_argument('--len_th', type=int, default=1, help="length threshold of k-mer matching region")
    args = parser.parse_args()
    exe_pool = Pool(args.n_core)

    candidate_file = args.candidate_file
    fasta_file = args.fasta_file
    lalign = args.lalign
    length_threshold = args.len_th

    fasta = FastaReader(fasta_file)
    seqs = {}
    for subread in fasta:
        seqs[subread.name] = subread.sequence

    candidates = []
    with open(candidate_file, 'r') as f:
        for line in f:
            header, match_length = line.split(' ')
            match_length = match_length.strip()
            candidates.append( (header, match_length, seqs[header], lalign) )

    for res in exe_pool.imap(validate_candidate, candidates):
        if res[4] != 0:   # more strict
            print res
