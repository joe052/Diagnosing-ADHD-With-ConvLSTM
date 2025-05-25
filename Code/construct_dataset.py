import re
import os
import pandas as pd

def parse_dx(dx):
    if int(dx) == 0:
        return 0
    else:
        return 1
    
# base_dir = "../data"
# dataset_dir = "../data/model_data"

base_dir = r"D:/adhd-fmri"
dataset_dir = r"D:/adhd-fmri/model_data"  

files_list = []
for file in os.listdir(dataset_dir):
    nums = re.findall(r'\d+', file)
    file_id = None
    for num in nums: 
        if len(num) > 1: 
            file_id = int(num)
            
    files_list.append({"ScanDir ID": file_id, "Image": file} )

images_df = pd.DataFrame(files_list)
tsv_path = r"D:\Joe Workspace\Codespace\Github\Diagnosing-ADHD-With-ConvLSTM\References\adhd200_preprocessed_phenotypics.tsv"
references_path = r"D:\Joe Workspace\Codespace\Github\Diagnosing-ADHD-With-ConvLSTM\References"

adhd_info = pd.read_csv(tsv_path, delimiter="\t")[['ScanDir ID','DX']]

model_data = adhd_info.merge(images_df, on='ScanDir ID')

for index,row in model_data.iterrows():
    if row['DX'] == 'pending':
        model_data.drop(index,axis=0,inplace=True)

model_data['DX'] = model_data['DX'].apply(parse_dx)

model_data.to_csv(os.path.join(references_path, "model_data.csv"), index=False)