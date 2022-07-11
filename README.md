# RBP-CAMAS
RBP-CAMAS is a classifier with Transformer to predict RNA-protein binding regeion on RNA. Input data are sequences of RNA (101nt) and protein molecule. Training data is made from RBPsuite (http://www.csbio.sjtu.edu.cn/bioinf/RBPsuite/)

# Code
Python scripts are in the python folder. The main script is /python/single_node/single_node.py Preprocessing scripts are in 

# Dataset
## Training Data
Dataset is not included here. However, dataset is made from RBPsuite dataset with scripts in python folder. In the preprocessing, RBPsuite data is clustered, selected, shuffled. Then, three types of masks and potential matrices are added, and sequences are tokenized. You need to preprocess before running RBP. Please rename folder names according to your environment. See the flow chart data_flow.pdf for preprocessing. If you would like to test your data, it must be preprocessed, too. 

## Statistical Potential
![Potentials](../../data/statpots.png)
Optimized Statistical potential data is in the data folder (best_pot_subset1_nocv.csv). See the ordinate of the figure above for the annotation of the values.

# How to Run
## preprocessing
See the flow chart in data_flow.pdf
## Training
Sample script (No_pre_aug):

python python/single_node/single_node.py \
    --data_dir_name all5_small_tape \
    --node_name f \
    --num_of_node 1 \
    --use_TAPE_feature 0 \
    --use_attn_augument 1 \
    --two_d_softm 1 \
    --clip_coeff 0 \
    --two_d_softm_mul_row_count 1 \
    --keyword no_tape_aug \
    --datafiles_num 1000 \
    --max_epoch 100 \
    --run_on_local 0 \
    --batch_size 5 \
    --num_heads 2 \
    --usechpoint 1 \
    --init_lr 4 \
    --self_player_num 4 \
    --self_rlayer_num 4 \
    --cross_layer_num 1 \
    --rna_dff 128 \
    --pro_dff 128 \
    --cross_dff 64 \
    --num_accum_grad 50 \
    --training 1 \
    --max_pro_len 2805 \
    --roc_data_log 1 \
    --group_to_ignore 0 \
    --only_rna_path 0 \
    --only_protein_path 0 \
    --data_mode all

## Test
Change training from 0 to 1, and change data_dir_name to the folder of data set you preprocessed in advance.

# Prerequisite
* Python 3.6.5
* Tensorflow 2.4.1
* MMseqs2 https://github.com/soedinglab/MMseqs2


# References
RBPsuite: Pan, X., Fang, Y., Li, X., Yang, Y., & Shen, H. B. (2020). RBPsuite: RNA-protein binding sites prediction suite based on deep learning. BMC genomics, 21(1), 1-8.
Transformer: Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. "Attention is all you need." Advances in neural information processing systems 30 (2017).
