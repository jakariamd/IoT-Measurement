This directory includes scripts to device selection and categorization (Section 4.3).

| File/Directory Name                | Description                                                                                                                            |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Device Categorization.ipynb        | This scrip labels devices to the generic device category. (Device type -> Device category) mapping is used to do the category labeling |
| Device Selection.ipynb             | This script extract unique IoT devices from manually identified and gpt identified devices.                                            |
| Device Unique Products.ipynb       | This script find number of unique products in the dataset (Table 1)                                                                    | 
| Get Subsidiary Organizations.ipynb | Finds subsidiary organization names of a given vendor                                                                                  | 
| Statistics.ipynb                   | Get number of devices in each category (Table 3)                                                                                       |


Run the script in the same order presented in the table to mimic the result
presented in the paper. Remember to uncomment any code line in the file (marked with ```\todo```)
to save collect data for entire domain set or to save data in file.


To run scripts
```bash
cd <code directory>
jupyter nbconvert --execute --to html --no-input <script-name>"
```
