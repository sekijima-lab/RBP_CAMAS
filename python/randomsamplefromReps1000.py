# -------------------------------------------------------------------
# this code random samples from rep files of MMseqs
# input : "/Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite/AARSnegativefa_rep_seq.fasta"
# output: "/Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite/82/"
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import os
import numpy as np

# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
SAMPLENUM = 40000
mode = "all"  # all or lnc
if mode == "all":
    ipath = "/Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite/"
    opath = f"/Users/mac/Documents/transformer_tape_dnabert/data/clusteredRBPsuite/{SAMPLENUM}/"
if not os.path.exists(opath):
    os.mkdir(opath)

# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------


def get_array(path):
    arr = []
    with open(path) as f:
        for lines in f.readlines():
            if ">" not in lines:
                arr.append(lines.strip())
    return np.array(arr)


def main():
    for file in os.listdir(ipath):
        if len(file) < 10:
            continue
        arr = get_array(f"{ipath}{file}")
        np.random.shuffle(arr)
        np.save(f"{opath}{file}", arr[:SAMPLENUM])
        # break


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    main()