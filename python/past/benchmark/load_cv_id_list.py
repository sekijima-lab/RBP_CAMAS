# -------------------------------------------------------------------
# this code 
# input : 
# output: 
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import numpy as np

# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
listfile = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/data/benchmarks/id_list_RPI369_for_5CV.csv.npz"

# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------


def main():
    arr = np.load(listfile, allow_pickle=True)
    print(arr.files)
    print(arr["list"][0])
    print(len(arr["list"][0]))


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    main()