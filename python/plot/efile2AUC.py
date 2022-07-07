# -------------------------------------------------------------------
# this code takes information from logs

# -------------------------------------------------------------------

# -------------------------------------------------------------------
# import
# -------------------------------------------------------------------
import os

import numpy as np
from sklearn import metrics
from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot as plt
# -------------------------------------------------------------------
# constant
# -------------------------------------------------------------------
dirpath = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/batchfiles/single_node/"
dirpath2 = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/batchfiles/unknown/"
figpath = "/Users/mac/Desktop/t3_mnt/transformer_tape_dnabert/plot/optimization/"
exp_name_dict = {"tape_aug_only_pro": "Only_pro", "tape_aug_clip": "Clip_coeff", "tape_aug_only_rna": "Only_RNA",
                 "tape_aug_no_2dsfot": "1D_softmax", "tape_aug_augmultiply": "Aug_prod",
                 "no_tape_no_aug": "No_pre_no_aug", "tape_aug": "Full", "tape_no_aug": "No_aug",
                 "only_lncRNA": "lnc_RNA", "no_tape_aug": "No_pre"}

unknown_list = ["0", "1", "2", "3", "4"]

exp_name_dict_rev = {"Only_pro": "tape_aug_only_pro", "Clip_coeff": "tape_aug_clip", "Only_RNA": "tape_aug_only_rna",
                     "1D_softmax": "tape_aug_no_2dsfot", "Aug_prod": "tape_aug_augmultiply",
                     "No_pre_no_aug": "no_tape_no_aug", "Full": "tape_aug", "No_aug": "tape_no_aug",
                     "lnc_RNA": "only_lncRNA", "No_pre": "no_tape_aug"}

grouplist = [["Full", "No_pre", "No_aug", "No_pre_no_aug"], ["Full", "1D_softmax", "No_aug"],
             ["Full", "Only_RNA", "Only_pro"], ["Full", "Clip_coeff", "lnc_RNA", "Aug_prod"]]

linestyle_list = ["-", ":", "-", "-", ":"]
linewidth_list = [3.5, 1.0, 1, 2, 2]
# -------------------------------------------------------------------
# function
# -------------------------------------------------------------------
plt.rcParams["font.size"] = 13


def avg2actnum(value, steps, sofar_sum):
    return value * steps - sofar_sum


def get_epoch_values(filenum, linelist):
    subauclist, sublosslist = [], []
    maxepoch = len(linelist)//filenum + 1
    epochcount = 0
    pred_arr = None  # for last epoch
    label_arr = None  # for last epoch
    for i in range(maxepoch - 1):  # epoch number is "i"
        start = filenum * i
        end = start + filenum
        totalstep = 0

        pred_arr = None  # for last epoch
        label_arr = None  # for last epoch

        for lines in linelist[start: end]:
            totalstep += 1
            listt, sublist = [], []
            line1 = lines.split(":")[2].split("]-")[0].strip("]").split("[")
            list1 = [x.strip("'").strip(" ").strip("]").replace("  ", " ") for x in line1][2:]
            list1 = [x[:-1] if x[-1] == " " else x for x in list1]
            list1 = [x.split(" ") for x in list1]
            for x in list1:
                for y in x:
                    if len(y) > 0:
                        sublist.append(y)
                listt.append(sublist)
                sublist = []
            list1 = [[float(e) for e in x] for x in listt]
            line2 = lines.split(":")[2].split("or(")[1]
            list2 = line2.split(",")[0]
            list2 = [x.strip("  [").split(" ") for x in list2.strip("[[[").split("]") if x]
            list2 = [[int(x) for x in item] for item in list2]
            # make two arrays for AUC caculation
            if totalstep == 1:
                pred_arr = np.array(list1)
                label_arr = np.array(list2)
            else:
                pred_arr = np.concatenate([pred_arr, np.array(list1)])
                label_arr = np.concatenate([label_arr, np.array(list2)])
            # calc. AUC and save to lists, the end of epoch
            if totalstep == filenum:
                subauclist.append(metrics.roc_auc_score(label_arr[:, 1], pred_arr[:, 1]))
                sublosslist.append(metrics.log_loss(label_arr, pred_arr))
                epochcount += 1
                totalstep = 0
    return subauclist, sublosslist, pred_arr, label_arr


def get_plot_data(mode, logpath, fold=None):  # {logpath}/tape_aug.e4323444, work for multiple files
    filecount, file_num_per_epoch = 0, 0
    keyw = None
    subauclist_all, sublosslist_all, pred_arr, label_arr = [], [], None, None
    if mode == "Test":
        keyw = "test ROC"
        file_num_per_epoch = 200
    elif mode == "Train":
        keyw = "train ROC"
        if not fold:
            file_num_per_epoch = 1000
        else:
            file_num_per_epoch = 800

    # --------------------------------------------------------
    # obtain information of e-files and sort them by date
    # --------------------------------------------------------
    if fold is not None:
        file_key = f"_{fold}.e"
    else:
        file_key = ".e"
    efilelist = [x for x in os.listdir(logpath) if file_key in x]
    datelist = [int(x.split(file_key)[1]) for x in os.listdir(logpath) if file_key in x]
    datelist.sort()

    # --------------------------------------------------------
    # get the last epoch labels & predictions, and all epoch auc and loss values
    # --------------------------------------------------------
    for datestr in datelist:
        for files in efilelist:
            if str(datestr) in files:
                linelist = []
                with open(f"{logpath}{files}") as f:
                    for lines in f.readlines():
                        if keyw in lines:
                            linelist.append(lines.strip())
                # collect date per file (about 30 epochs), list for 30 epochs, arr for 1 epoch
                subauclist, sublosslist, pred_arr, label_arr = get_epoch_values(file_num_per_epoch, linelist)
                subauclist_all += subauclist
                sublosslist_all += sublosslist
                filecount += 1

    return [sublosslist_all, subauclist_all, label_arr, pred_arr]


def group_plot(plotdata, phasetype, expnames, gr_idx):
    # plotdata = [{"Train": [losslist, auclist, labels, preds], "Test": [losslist, auclist, labels, preds]},
    #             {Train": [losslist, auclist, labels, preds], "Test": [losslist, auclist, labels, preds]}, ...]

    # --------------------------------------------------------
    # LOSS plot
    # --------------------------------------------------------
    fig, ax = plt.subplots()
    for idx, sublist in enumerate(plotdata):
        ax.plot(range(len(sublist[phasetype][0])), sublist[phasetype][0], label=expnames[idx], linestyle=linestyle_list[idx],
                linewidth=linewidth_list[idx])
    ax.grid(visible=True, axis="y")
    fig_name = f"group_{gr_idx}_{phasetype}_loss.png"
    # plt.title(f"{phasetype} Loss")
    plt.ylabel("Loss", fontsize=15)
    plt.xlabel("Epoch", fontsize=15)
    ax.legend()
    plt.savefig(f"{figpath}{fig_name}")
    plt.show()

    # --------------------------------------------------------
    # AUC plot
    # --------------------------------------------------------
    fig, ax = plt.subplots()
    for idx, sublist in enumerate(plotdata):
        plt.plot(range(len(sublist[phasetype][1])), sublist[phasetype][1], label=expnames[idx], linestyle=linestyle_list[idx],
                linewidth=linewidth_list[idx])
    ax.grid(visible=True, axis="y")
    # plt.title(f"{phasetype} AUROC")
    plt.ylabel("AUROC", fontsize=15)
    plt.xlabel("Epoch", fontsize=15)
    fig_name = f"group_{gr_idx}_{phasetype}_AUROC.png"
    plt.ylim(0.5, 1)
    ax.legend()
    plt.savefig(f"{figpath}{fig_name}")
    plt.show()

    # --------------------------------------------------------
    # ROC plot
    # --------------------------------------------------------
    fig, ax = plt.subplots()
    for idx, sublist in enumerate(plotdata):
        label_arr = sublist[phasetype][2]
        pred_arr = sublist[phasetype][3]
        rocd = roc_curve(label_arr[:, 1], pred_arr[:, 1])
        rocscore = roc_auc_score(label_arr[:, 1], pred_arr[:, 1])
        ax.plot(rocd[0], rocd[1], label=f"{expnames[idx]} ({round(rocscore, 4)})", linestyle=linestyle_list[idx],
                linewidth=linewidth_list[idx])
    fig_name = f"group_{gr_idx}_{phasetype}_AUROC.png"
    # plt.title(f"{phasetype} ROC")
    plt.xlabel("False Positive Rate", fontsize=15)
    plt.ylabel("True Positive Rate", fontsize=15)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    ax.legend()
    plt.savefig(f"{figpath}{fig_name}")
    plt.show()


# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------
if __name__ == '__main__':
    # -----------------------------
    # Ablation
    # -----------------------------
    for gidx, explist in enumerate(grouplist):
        datalist = []

        # obtain data for plot
        for expname in explist:  # per experiment such as Full
            dirname = exp_name_dict_rev[expname]
            plot_data_dict = {}
            for phase in ["Train", "Test"]:
                plot_data_dict[phase] = get_plot_data(phase, f"{dirpath}{dirname}/")
            datalist.append(plot_data_dict)

        # plot for each phase(Train or Test)
        for phase in ["Train", "Test"]:
            group_plot(datalist, phase, explist, gidx)
        # break

    # -----------------------------
    # Unknown Proteins
    # -----------------------------
    # obtain data for plot
    datalist = []
    for foldid in range(5):  # perrange experiment such as Full
        plot_data_dict = {}
        for phase in ["Train", "Test"]:
            plot_data_dict[phase] = get_plot_data(phase, f"{dirpath2}", foldid)
        datalist.append(plot_data_dict)
    # plot for each phase(Train or Test)
    for phase in ["Train", "Test"]:
        group_plot(datalist, phase, unknown_list, 4)
    # break