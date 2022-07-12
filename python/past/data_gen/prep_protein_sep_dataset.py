# -------------------------------------------------------------------
# this code writes token list of [RNA and protein and label]
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import os, sys
import numpy as np

# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
group = 0

# ------------------------  CHECK AND CHANGE HERE IF NECESSARY !!!!!!
mode = "all_unknown_protein"  # all or lnc or all_unknown_protein
# ---------------------------------------

count_per_file = 5
# input = f"/Users/mac/Documents/transformer_tape_dnabert/train_dir/"
output = f"data/unknown_protein/"

if mode == "all":
    input2 = f"data/clusteredRBPsuite/82/"
    output_one = f"data/known_protein/"
elif mode == "lnc":
    input2 = f"data/clusteredRBPsuite_lncRNA_RNA_only/82/"
    output_one = f"data/known_protein_lncRNA/"
else: # all_unknown_protein
    input2 = f"data/clusteredRBPsuite/82/"
    output_one = f"data/unknown_protein_all/"

protein_cv_list_2805 = [['EIF3D', 'HNRNPL', 'BCLAF1', 'CPEB4', 'NSUN2', 'SMNDC1', 'AKAP8L', 'BCCIP', 'EIF3G', 'DDX24', 'METAP2', 'EIF4G2', 'LSM11', 'UCHL5', 'UTP18', 'AKAP1', 'SND1', 'DDX42', 'IGF2BP3', 'PTBP1', 'RBFOX2', 'GPKOW', 'SRSF7', 'STAU2', 'TAF15', 'SAFB2', 'ZC3H8', 'SF3B4', 'HNRNPA1', 'XRN2', 'SUGP2'], ['XPO5', 'LIN28B', 'NONO', 'SDAD1', 'ZNF622', 'SFPQ', 'SF3B1', 'UTP3', 'CPSF6', 'LARP7', 'NIPBL', 'ZRANB2', 'KHSRP', 'WRN', 'HNRNPC', 'SRSF1', 'EIF3H', 'ILF3', 'PPIG', 'CSTF2T', 'LARP4', 'SSB', 'AGGF1', 'U2AF2', 'SF3A3', 'YWHAG', 'FMR1', 'U2AF1', 'NCBP2', 'DKC1', 'TRA2A'], ['SERBP1', 'ZC3H11A', 'FXR2', 'FXR1', 'SUPV3L1', 'FKBP4', 'RPS11', 'GRSF1', 'ZNF800', 'SUB1', 'PPIL4', 'FUBP3', 'WDR3', 'NOLC1', 'UPF1', 'HNRNPU', 'HNRNPUL1', 'DROSHA', 'DDX52', 'QKI', 'AUH', 'TROVE2', 'DDX51', 'ABCF1', 'TBRG4', 'DDX21', 'XRCC6', 'GTF2F1', 'DGCR8', 'CDC40', 'MATR3'], ['PHF6', 'POLR2G', 'NIP7', 'WDR43', 'DHX30', 'FUS', 'MTPAP', 'NPM1', 'HNRNPK', 'SRSF9', 'PABPC4', 'PRPF4', 'DDX3X', 'RPS3', 'AATF', 'SBDS', 'DDX59', 'RBM15', 'DDX6', 'PUM2', 'EXOSC5', 'HLTF', 'RBM27', 'PUM1', 'PUS1', 'GEMIN5', 'GRWD1', 'RBM5', 'CSTF2', 'FTO', 'SLTM'], ['GNL3', 'EWSR1', 'AARS', 'NKRF', 'FAM120A', 'PCBP2', 'FASTKD2', 'EFTUD2', 'PRPF8', 'RBM22', 'IGF2BP2', 'BUD13', 'SAFB', 'TIAL1', 'NOL12', 'IGF2BP1', 'PCBP1', 'SLBP', 'AQR', 'DDX55', 'APOBEC3C', 'G3BP1', 'KHDRBS1', 'PABPN1', 'TARDBP', 'HNRNPM', 'TIA1', 'YBX3', 'RPS5', 'TNRC6A']]

proseq_master = f"data/proteinseqs.csv"

# >chr12:13080717-13080852(+)
# ACCGUAAGUCAAAGGUCAGACUGUCCAGUGGGUGAUCUCUCAAGUCGCCCGCUUGGCCUCUUCCAAGUGUACUUUACUUCCUUUCAUUCCUGCUCUAAAAC
# >chrY:2357424-2357563(-)
# AGGUGGCCGAGAUGCUGUCGGCCUCCAGGUACCCCACCAUCAGCAUGGUGAAGCCGCUGCUGCACAUGCUCCUGAACACCACGCUCAACAUCAAGGAGACC

# get all protein names from RBPsuite file names
# all_protein_list = []
# for files in os.listdir(input):
#     protein_name = files.split(".")[0]
#     if protein_name not in all_protein_list:
#         all_protein_list.append(protein_name)
#
# # split the names into five groups
# protein_cv_list_2805 = []
# for i in range(5):
#     # try:
#     protein_cv_list_2805.append(all_protein_list[31*i: 31*(i+1)])
#
# print((protein_cv_list_2805))
# for item in protein_cv_list_2805:
#     print(len(item))

# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------


def get_pro_id_dict():
    id = 0
    id_dict = {}
    for item in protein_cv_list_2805:
        for name in item:
            id_dict[name] = id
            id += 1
    return id_dict


def get_proseq(proname):
    sequence = None
    with open(proseq_master) as f:
        for lines in f.readlines():
            if proname in lines:
                sequence = lines.split(",")[1].strip()
    return sequence


def to_five_groups():
    rnaseq = ""
    pro_id_dict = get_pro_id_dict()
    for group in range(5):
        count = 0
        datalist = []
        print(protein_cv_list_2805[group])
        print(len(protein_cv_list_2805[group]))
        if not os.path.isdir(f"{output}{group}"):
            os.makedirs(f"{output}{group}")
        for file in os.listdir(input):
            protein_name = file.split(".")[0]
            if protein_name in protein_cv_list_2805[group]:
                count += 1
                print(count)
                proseq = get_proseq(protein_name)
                # if count % 10 == 0:
                if proseq is None:
                    print(f"{protein_name} not in list!")
                    continue
                with open(f"{input}{file}") as f:
                    for lines in f.readlines():
                        if ">" in lines:
                            if "negative" in file:
                                label = 0
                            else:
                                label = 1
                        else:
                            rnaseq = lines.strip()
                            datalist.append([pro_id_dict[protein_name], proseq, rnaseq, label])

        # arr = np.array(datalist)
        # np.random.shuffle(arr)
        # for i in range(900):
        #     np.save(f"{output}{group}/{i}", arr[i * count_per_file: (i + 1) * count_per_file])


def unknown_lncRNA_to_five():
    pro_id_dict = get_pro_id_dict()
    for group in range(5):
        filecount = 0
        final_arr = None
        for dir in os.listdir(input2):
            datalist = []
            if ".DS" in dir:
                continue
            if "negative" in dir:
                label = 0
                proname = dir.split("negative")[0]
            else:
                label = 1
                proname = dir.split("positive")[0]
            proid = pro_id_dict[proname]

            # if the protein belongs to the group, go on
            if proname in protein_cv_list_2805[group]:
                arr = np.load(f"{input2}{dir}")
                proseq = get_proseq(proname)
                for item in arr:
                    datalist.append([proid, proseq, item, label])
                arr = np.array(datalist)
                np.random.shuffle(arr)
                arr = arr[0:17]
                if filecount == 0:
                    final_arr = arr
                else:
                    final_arr = np.concatenate([final_arr, arr])
                filecount += 1
        np.random.shuffle(final_arr)

        print(f"final_arr is {final_arr.shape}")
        for i in range(1000):
            np.save(f"{output_one}{group}/{i}", final_arr[i * count_per_file: (i + 1) * count_per_file])


def to_one_group():
    for i in range(5):
        for j in range(900):
            arr = np.load(f"{output}{i}/{j}.npy")
            if i == 0 and j == 0:
                final_arr = arr
            else:
                final_arr = np.concatenate([final_arr, arr])

    np.random.shuffle(final_arr)
    for i in range(4500):
        # print(final_arr[i * count_per_file: (i + 1) * count_per_file].shape)
        np.save(f"{output_one}/{i}", final_arr[i * count_per_file: (i + 1) * count_per_file])


def clustered_to_one_group():
    pro_id_dict = get_pro_id_dict()
    count = 0
    for dir in os.listdir(input2):
        datalist = []
        if ".DS" in dir:
            continue
        arr = np.load(f"{input2}{dir}")
        if "negative" in dir:
            label = 0
            proname = dir.split("negative")[0]
        else:
            label = 1
            proname = dir.split("positive")[0]
        proid = pro_id_dict[proname]
        proseq = get_proseq(proname)
        for item in arr:
            datalist.append([proid, proseq, item, label])
        arr = np.array(datalist)
        if count == 0:
            final_arr = arr
        else:
            final_arr = np.concatenate([final_arr, arr])
        count += 1
        print(count)

    np.random.shuffle(final_arr)
    for i in range(5000):
        # print(final_arr[i * count_per_file: (i + 1) * count_per_file].shape)
        np.save(f"{output_one}/{i}", final_arr[i * count_per_file: (i + 1) * count_per_file])


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    # clustered_to_one_group()
    unknown_lncRNA_to_five()
