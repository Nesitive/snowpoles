import torch
import os

ROOT_PATH = '/datadrive/vmData/SNEX20_TLI_resized_clean'
    #OUTPUT_PATH = '/datadrive/vmData/snow_poles_outputs_resized_FT_5_LRe4_BS64_E100_clean_Aug' #snow_poles_outputs_resized_FT_10_LRe4_BS64_E100_clean'
OUTPUT_PATH = '/datadrive/vmData/snow_poles_outputs_resized_LRe4_BS64_E10000_clean_SNEX_IN_wOK_8020' #snow_poles_outputs_resized_FT_10_LRe4_BS64_E100_clean'
    #OUTPUT_PATH = '/datadrive/vmData/snow_poles_outputs_resized_LRe5_BS64_E100_clean'
snowfreetbl_path = '/datadrive/vmData/snowfree_table.csv'
manual_labels_path = '/datadrive/vmData/manuallylabeled_CUBM02corr.csv' #'/datadrive/vmData/SNEX20_SD_TLI_clean.csv'
datetime_info = '/datadrive/vmData/labeledImgs_datetime_info.csv' #'/datdrive/vmData/native_res/native_res'
native_res_path = '/datadrive/vmData/nativeRes.csv'

# learning parameters
BATCH_SIZE = 64 #64 #4 #32
LR = 0.0001 #0.00001  # #0.0001 lower to factor of 10
EPOCHS = 10000 #100
#DEVICE = torch.device('mps')  #should be cuda on VMs
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# train/test split
TEST_SPLIT = 0.2  ## could update for the cameras that we want to hold out as validation
# show dataset keypoint plot
SHOW_DATASET_PLOT = False
AUG = False ## True for Aug; False for None

keypointColumns = ['x1', 'y1', 'x2', 'y2'] ## update

# Fine-tuning set-up
FINETUNE = False ## True for test/val dataset to be the subset 
FT_PATH = '/datadrive/vmData/snow_poles_outputs_resized_LRe4_BS64_E100_clean_SNEX_IN' ## model that you want to fine tune
FT_sample = 10
FT_IMG_PATH = '/datadrive/vmData/WAsubset_every10'
