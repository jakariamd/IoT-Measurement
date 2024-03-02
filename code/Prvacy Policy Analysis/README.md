This directory contains scripts used to analyze privacy policies collected by MAPS [81]
crawler (Section 6.2)

| File/Directory Name   | Description                                             |
|-----------------------|---------------------------------------------------------|
| Data Processing.ipynb | Preprocess privacy policy data collected by MAPS [81]   |
| Policy Analysis.ipynb | Analyze privacy policy using fine-tuned PrivBERT model. |

Tuning PrivBERT model with OPP-115 dataset can be found here: https://www.kaggle.com/code/jakariamd/opp-15-binary-classifier-genaralised
Use [environment_tf_gpu_cuda8.yml](environment_tf_gpu_cuda8.yml) environment to run the Policy Analysis Script. 


Run the script in the same order presented in the table to mimic the result
presented in the paper. Remember to uncomment any code line in the file (marked with ```\todo```)
to save collect data for entire domain set or to save data in file.


To run scripts
```bash
cd <code directory>
jupyter nbconvert --execute --to html --no-input <script-name>"
```