# AdaptorFinder
tools that find adaptor unremoved subreads

## Usage

this programs need `pbcore` in the virtual environment, and `lalign` for `validate_unremoved_adaptor.py`.

```
usage: find_candidates.py [-h] [--n_core N_CORE] [--len_th LEN_TH] fasta_file

find candidates of subreads adaptor unremoved

positional arguments:
  fasta_file       a file that contains the subread information

optional arguments:
  -h, --help       show this help message and exit
  --n_core N_CORE  number of processes
  --len_th LEN_TH  length threshold of k-mer matching region
```

```
usage: validate_unremoved_adaptor.py [-h] [--lalign LALIGN] [--n_core N_CORE]
                                     [--len_th LEN_TH]
                                     candidate_file fasta_file

validate the candidates and get alignments between the plus strand and the
minus strand

positional arguments:
  candidate_file   a file that lists candidates of adaptor unremoved subreads
  fasta_file       a file that contains the subread information

optional arguments:
  -h, --help       show this help message and exit
  --lalign LALIGN  the directory of lalign
  --n_core N_CORE  number of processes
  --len_th LEN_TH  length threshold of k-mer matching region
```

## Example

```
$ source VIRTUAL_ENV_DIR/bin/activate
$ python find_candidates.py --n_core 12 --len_th 35 subreads.fasta > candidates
$ python validate_unremoved_adaptor.py --n_core 12 --lalign LALIGN_DIR candidates subreads.fasta > overlap
```