This directory includes scripts to validate device identification and endpoint categorization approaches (Section 4.2 and Section 5.1-5.3).

| File/Directory Name                      | Description                                                                                                                 |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Device Identification                    | Contains scripts for validating device identification methods                                                               |
| Endpoint Mapping Manual Validation.ipynb | Samples 100 endpoints mapping result from each category for manual validation                                               |


Run the script in the same order presented in the table to mimic the result
presented in the paper. 
Remember to uncomment any code line in the file (marked with ```\todo```)
to save collect data for entire domain set or to save data in file.


To run scripts
```bash
cd <code directory>
jupyter nbconvert --execute --to html --no-input <script-name>"
```
