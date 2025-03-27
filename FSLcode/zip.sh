#好像基于gzip暴力压缩nii文件会导致fsl读取不了，所以不用这个脚本
#start_dir="/research/Re/Painlearning/data"
#cd "$start_dir" || exit

#find "$start_dir" -type f -name "*.nii" -print0 | while IFS= read -r -d '' file; do
#    gzip -k "$file"
#    echo "Compressed $file to ${file%.nii}.nii.gz"
#done

#!/bin/bash

# 采用fsl自带的格式转换工具批量压缩
#!/bin/bash

#!/bin/bash

input_dir="/research/Re/Painlearning/data"
find "$input_dir" -type f -name '*.nii' | while read file; do
  filename=$(basename "$file")
  filename_without_ext="${filename%.*}"
  output_file="${file%.nii}.nii.gz"
  fslchfiletype NIFTI_GZ "$file" "$output_file"
  rm "$file"  # 删除原文件
  echo "$filename 成功转换成nii.gz文件。"
done
echo "所有文件转换完成。"