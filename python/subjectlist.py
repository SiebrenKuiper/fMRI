import os

def get_subject_run_info(bids_dir):
    sj_ls = [f.split('-')[1] for f in os.listdir(bids_dir) if f.startswith('sub') and not f.endswith('.html')]
    sj_to_fl = {sj: [] for sj in sj_ls}
    for j in sj_ls:
        fl = [f[20:22] for f in os.listdir(os.path.join(bids_dir, f"sub-{j}", "func")) if f.endswith("bold.nii.gz")]
        sj_to_fl[j] = fl
    return sj_to_fl