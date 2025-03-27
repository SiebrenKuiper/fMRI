import os
import shutil
from nilearn import image
import nibabel

def smooth_fmri_data(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            src_file_path = os.path.join(root, file)
            if 'func' in root and file.endswith('bold.nii.gz'):
                try:
                    img = image.load_img(src_file_path)
                    #移除前四个伪扫描
                    img = img.slicer[:, :, :, 4:]
                    smooth_img = image.smooth_img(img, fwhm=8)
                    smooth_img_path = src_file_path.replace('.nii.gz', '_smooth.nii.gz')
                    smooth_img.to_filename(smooth_img_path)
                    print(f"Smoothed file: {smooth_img_path}")
                except Exception as e:
                    print(f"Error processing {src_file_path}: {e}")

input_directory = '/research/Re/Painlearning/derivatives/preprocessed'
smooth_fmri_data(input_directory)