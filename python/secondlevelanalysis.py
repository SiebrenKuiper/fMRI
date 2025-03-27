# -*- coding: utf-8 -*-
# @platform: Windows subsystem for Linux, Ubuntu-22.04
# @environment: python=3.10, nilearn=0.10.4
# author: Zhao-Penggeng
# software: Microsoft Visual Code

from subjectlist import get_subject_run_info
from nilearn.glm.second_level import SecondLevelModel
from nilearn import image
from nilearn import plotting
import pandas as pd
import glob
import nibabel as nib
import os
import numpy as np

base_dir = "/research/Re/Painlearning/derivatives/preprocessed"
subjectinfo = get_subject_run_info(base_dir)

high_low = []
low_high = []

# 确保输出目录存在
fitstlevel_dir = "/research/Re/Painlearning/derivatives/firstlevelresult"
secondlevel_dir = "/research/Re/Painlearning/derivatives/secondlevelresult"
if not os.path.exists(secondlevel_dir):
    os.makedirs(secondlevel_dir)

for contrast_id in ["high_low", "low_high"]:
    for sj in subjectinfo:
        # 构造正确的文件路径模式
        file_pattern = os.path.join(fitstlevel_dir , f'sub-{sj}_run*_{contrast_id}.nii')
        file_paths = glob.glob(file_pattern)
        if file_paths: 
            concatenated_image = image.mean_img(file_paths)
            nii_file_path = os.path.join(secondlevel_dir, f"sub-{sj}_{contrast_id}.nii")
            nib.save(concatenated_image, nii_file_path)
            if contrast_id == "high_low":
                high_low.append(nii_file_path)
            else:
                low_high.append(nii_file_path)
        else:
            print(f"No files found for subject {sj} with contrast {contrast_id}")

# 创建设计矩阵，只包含截距项
n_subjects = len(subjectinfo)
design_matrix = pd.DataFrame({
    'Intercept': np.ones(n_subjects)
})
# 创建第二水平模型并拟合数据
slm_method = SecondLevelModel()
second_level_model = slm_method.fit(high_low, design_matrix=design_matrix)
z_map = second_level_model.compute_contrast(second_level_contrast='Intercept',output_type="z_score")
plotting.plot_stat_map(z_map, display_mode="mosaic", threshold=3.0, cut_coords=3, title=contrast_id, black_bg=True,colorbar=True,
                                   output_file=os.path.join(secondlevel_dir, f"high_low_result.png"))
high_low_path = os.path.join(secondlevel_dir, f"high_low_result.nii")
nib.save(z_map, high_low_path)
# 如果需要对low_high进行分析，可以再次使用SecondLevelModel
# slm_method2.fit(low_high, design_matrix=design_matrix)