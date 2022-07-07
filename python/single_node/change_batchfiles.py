# -------------------------------------------------------------------
# this code changes flags in batch files
# input : 
# output: 
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import os, shutil

# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
path = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/batchfiles/single_node/"
path2 = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/batchfiles/unknown/"

# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------


def correct_contents(fpath):
    with open(fpath) as f, open(f"{fpath}.tmp", "w") as fo:
        for lines in f.readlines():
            if "_node=" in lines:  # #$ -l f_node=1
                fo.writelines(lines.replace("q_node", "f_node"))
            elif "node_name" in lines:  # -node_name f
                fo.writelines(lines.replace(" q", " f"))
            elif "usechpoint" in lines:
                fo.writelines(lines.replace(" 0", " 1"))
            else:
                fo.writelines(lines)


def search_and_change(dir):
    batchfile = ""
    for files in os.listdir(dir):
        if "test_" in files and "tmp" not in files:
            batchfile = f"{dir}/{files}"
            shutil.copy2(batchfile, f"{batchfile}.tmp")
            correct_contents(batchfile)
            shutil.copy2(f"{batchfile}.tmp", batchfile)
            os.remove(f"{batchfile}.tmp")


def main():
    for dir in os.listdir(path):
        if "past" not in dir and "zip" not in dir:
            search_and_change(f"{path}{dir}")
    # search_and_change(path2)


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    main()