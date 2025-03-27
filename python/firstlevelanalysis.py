# -*- coding: utf-8 -*-
# @platform: Windows subsystem for Linux, Ubuntu-22.04
# @environment: python=3.10, nilearn=0.10.4
# author: Zhao-Penggeng
# software: Microsoft Visual Code
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from nilearn.glm.first_level import FirstLevelModel
from nilearn import image, plotting
from subjectlist import get_subject_run_info

def create_first_level_model(fmridata, confdata, eventdata, output_dir, sj, fl):
    fmri_img = image.load_img(fmridata)
    confounds = pd.read_csv(confdata, sep='\t')
    confoundlist = confounds.loc[:, ['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
    events = pd.read_csv(eventdata, sep='\t')
    flm = FirstLevelModel(t_r=2, drift_model="polynomial", drift_order=5, smoothing_fwhm=8)
    first_level_model = flm.fit(fmri_img, events=events, confounds=confoundlist)
    design_matrix = first_level_model.design_matrices_[0]
    fig, ax = plt.subplots(figsize=(12, 8))
    plotting.plot_design_matrix(design_matrix, ax=ax)
    ax.get_images()[0].set_clim(0, 0.2)
    design_matrix_filename = os.path.join(output_dir, f"sub-{sj}_run-{fl}_design_matrix.png")
    plt.savefig(design_matrix_filename, dpi=300)
    plt.close(fig)
    return flm, first_level_model, design_matrix

def make_localizer_contrasts(design_matrix):
    contrast_matrix = np.eye(design_matrix.shape[1])
    contrasts = {
        column: contrast_matrix[i]
        for i, column in enumerate(design_matrix.columns)
    }
    if "high" in design_matrix.columns and "low" in design_matrix.columns:
        contrasts["high_low"] = contrasts["high"] - contrasts["low"]
        contrasts["low_high"] = contrasts["low"] - contrasts["high"]
    return contrasts

def save_contrast_images(first_level_model, contrasts, output_dir, sj, fl):
    selected_contrasts = ["high_low", "low_high"]
    for contrast_id in selected_contrasts:
        if contrast_id in contrasts:
            contrast_val = contrasts[contrast_id]
            z_map = first_level_model.compute_contrast(contrast_val, output_type="z_score")
            plotting.plot_stat_map(z_map, display_mode="mosaic", threshold=3.0, cut_coords=3, title=contrast_id, black_bg=True,
                                   output_file=os.path.join(output_dir, f"sub-{sj}_run-{fl}_{contrast_id}.png"))
            nii_file_path = os.path.join(output_dir, f"sub-{sj}_run-{fl}_{contrast_id}.nii")
            nib.save(z_map, nii_file_path)

def main():
    base_dir = "/research/Re/Painlearning/derivatives/preprocessed"
    output_dir = "/research/Re/Painlearning/derivatives/firstlevelresult"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    sj_to_fl = get_subject_run_info(base_dir)
    for j, fl_list in sj_to_fl.items():
        print(f"sj: {j}, fl: {fl_list}")
        for fl in fl_list:
            fmridata = os.path.join(base_dir, f"sub-{j}", "func", f"sub-{j}_task-tsl_run-{fl}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz")
            eventdata = os.path.join("/research/Re/Painlearning/data", f"sub-{j}", "func", f"sub-{j}_task-tsl_run-{fl}_events.tsv")
            confdata = os.path.join(base_dir, f"sub-{j}", "func", f"sub-{j}_task-tsl_run-{fl}_desc-confounds_timeseries.tsv")
            flm, first_level_model, design_matrix = create_first_level_model(fmridata, confdata, eventdata, output_dir, j, fl)
            contrasts = make_localizer_contrasts(design_matrix)
            save_contrast_images(first_level_model, contrasts, output_dir, j, fl) 

if __name__ == "__main__":
    main()