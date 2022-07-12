# -------------------------------------------------------------------
# this code run mmseqs2 for all fasta file of RBPsuite
# mmseqs easy-linclust /Users/mac/Downloads/train_dir/AARS.negative.fa clusterRes tmp
# input : /Users/mac/Downloads/train_dir/AARS.negative.fa
# output: /Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import os
from subprocess import call
# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
# --------- all ----------
# ipath = "/Users/mac/Documents/transformer_tape_dnabert/train_dir/"
# opath = "/Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite"

# --------- lncRNA only ----------
ipath2 = "data/lncRNA_in_RBPsuite/"
ipath = "data/lncRNA_in_RBPsuite/with_headers/"
opath = "data/clusteredRBPsuite_lncRNA_RNA_only/"

# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------


def make_ifile_with_headers():
    for files in os.listdir(ipath2):
        count = 0
        if os.path.isdir(f"{ipath2}{files}"):
            continue
        with open(f"{ipath2}{files}") as f, open(f"{ipath}{files}", "w") as fo:
            for lines in f.readlines():
                fo.writelines(f">entry_{count}\n{lines}")
                count += 1


def main():
    os.chdir(opath)
    for files in os.listdir(ipath):
        if os.path.isdir(f"{ipath}{files}"):
            continue
        call([f"mmseqs easy-linclust {ipath}{files} {files.replace('.', '')} tmp"], shell=True)
        os.remove(f"{files.replace('.', '')}_all_seqs.fasta")
        os.remove(f"{files.replace('.', '')}_cluster.tsv")
        call([f"rm -Rf ./tmp"], shell=True)
        # break

# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    # if lncRNA make files with headers
    make_ifile_with_headers()
    main()
