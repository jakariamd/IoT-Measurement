## **Connecting the Dots: Tracing Data Endpoints in IoT Devices**


### Abstract
Smart home devices are constantly exchanging data with a variety of remote endpoints.
This data encompasses diverse information, from device operation and status to sensitive user information like behavioral usage patterns.
However, there is a lack of transparency regarding where such data goes and with whom it is potentially shared.  
This paper investigates the diverse endpoints that smart home Internet-of-Things (IoT) devices contact to better understand and reason about the IoT backend infrastructure, thereby providing insights into potential data privacy risks.
We analyze data from 5,413 users and 25,123 IoT devices using the IoT Inspector, an open-source application allowing users to monitor traffic from smart home devices on their networks.
First, we develop semi-automated techniques to map remote endpoints to organizations and their business types to shed light on their potential relationships with IoT end products.
We discover that IoT devices contact more third or support-party domains than first-party domains.
We also see that the distribution of contacted endpoints varies based on the user's location and across vendors manufacturing similar functional devices, where some devices are more exposed to third parties than others.
Our analysis also reveals the major organizations providing backend support for IoT smart devices and provides insights into the temporal evolution of cross-border data-sharing practices.

### Security/Privacy Issues and Ethical Considerations
As this is a paper focused on measurements, the majority of the metrics pertain to the quantity of users, devices, or endpoints. These quantities are determined by tallying the personally identifiable information (PIIs), such as device IDs or user IDs. In consideration of user privacy and ethical concerns, we have opted not to include the complete dataset in this artifact. Consequently, some of the analysis results may not be fully reproducible.
**Why we don’t want to share the original raw data in public:** Although we never intended to collect PIIs when we first deployed IoT Inspector ([LINK](https://doi.org/10.1145/3397333)), we have inadvertently collected PIIs; we never realized that IoT devices leaked PIIs in local communications until recently ([LINK](https://doi.org/10.1145/3618257.3624830)). These PIIs may, for instance, include the first names of the users in mDNS or UPnP messages. Even if a device does not support local communications such as mDNS or UPnP, an attacker, with the original dataset, could still, in theory, de-anonymize individuals because the original dataset includes persistent identifiers of devices and users. Theoretically, an attacker, for instance, could (e.g., through social engineering) convince a victim to open a special TV app under the attacker’s control and also run IoT Inspector; the victim opens the app on their TV; the app communicates with a special hostname; the hostname appears in the IoT Inspector dataset; the attacker obtains the dataset and looks for the special hostname; the attacker identifies the associated device ID and user ID; the attacker discovers all TV activities (based on the TV’s device ID), identifies the other IoT devices, and analyzes all IoT activities (based on the user ID), problematic especially if the victim has sensitive devices (e.g., medical devices, sex toys, etc). Because of the reasons above, we are withholding the following fields from the public dataset: any local communications such as mDNS and UPnP messages; device IDs; and user IDs. Researchers interested in obtaining the full dataset may contact us and seek the approval from the IRBs of respective institutions before we can share the full dataset.
Interested readers could also read [this](https://www.cs.utexas.edu/~shmat/shmat_oak08netflix.pdf) paper that shows potential risks of publishing similar datasets.


## Basic Requirements

### Hardware Requirements
Processor:	11th Gen Intel(R) Core(TM) i7-11700 @ 2.50GHz   2.50 GHz\
RAM:	32.0 GB\
GPU:	GeForce RTX 3060 (For faster privacy policy analysis using BERT model)\

### Software Requirements
System type:	64-bit operating system, x64-based processor\
Anaconda \
DataSpell (Optional)\
Tensorflow 2.3\
Cuda Toolkit 9


### Estimated Time and Storage Consumption
The estimated time for each test is at most 20 minutes, and the storage consumption is at most 40GB.
## Environment

### Accessibility

GitHub repository: Clone the repository: https://github.com/jakariamd/IoT-Measurement.git 
commit-id or tag:

### Set up the environment
Install Anaconda from [here](https://docs.anaconda.com/free/anaconda/install/index.html) 

Clone the repository from Anaconda Prompt:
```bash
git clone https://github.com/jakariamd/IoT-Measurement.git
```
```
cd IoT-Measurement
conda env create -f environment_iot.yml
conda activate iot
pip install -U spacy
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
```


### Testing the Environment
Once the environment is created, run the following commands. If the environment is set properly, these commands will run Domain2Org (Python Whois).ipynb script and produce an html file containing a table of 10 rows.

```bash
cd "code/Endpoint Mapping/First Party Mapping/"
jupyter nbconvert --execute --to html --no-input "Domain2Org (Python Whois).ipynb"
```
Note: Update the chromedriver in "code/Endpoint Mapping/First Party Mapping/" according to your system. 

## Directories' description
| Directory                                  | Description                                                                                                         |
|:-------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|
| `code/Device Identification`               | Implementations of the  device identification methodologies (Section 4.2)                                           |
| `code/Device Selection and Categorization` | Implementations of the methodologies (Section 4.3)                                                                  |
| `code/Endpoint Mapping`                    | Implementations of the Endpoints Categorization (Section 5).                                                        |
| `code/Validation`                          | Scripts to validate device identification and endpoint categorization approaches (Section 4.2 and Section 5.1-5.3). |
| `code/Validation/Device Identification`    | Scripts to validate device identification (Section 4.2).                                                            |
| `code/Analysis`                            | Scripts for result analysis (Section 6, except the privacy policy analysis described in section 6.2)                |
| `code/Prvacy Policy Analysis`              | Scripts for privacy policy analysis (described in section 6.2)                                                      |
|                                            |                                                                                                                     |
| `Inspector Data/New data`                  | Redacted IoT-Inspector data (dataset used in this paper, PIIs excluded Section 3)                                   |
| `Device Identification`                    | Data generated by Device Identification methods (Section 4)                                                         |
| `Endpoint Mapping Data`                    | Data collected for endpoint mapping (Section 5)                                                                     |
| `Validation Data`                          | Data for validating device identification and endpoint categorization methods (Section 4.2 and Section 5.1-5.3)     |
| `Statistical Data`                         | Various statistics generated by analysis scripts (Section 6)                                                        |
| `Domain Block Lists`                       | Various block lists used in endpoint analysis (Section 6.1)                                                         |
| `MAPS Output`                              | Privacy policy data collected by MAPS approach (Section 6.2)                                                        |


***Guidance on mimicking various sections of the document is available in the 
readme.md files located within the respective code directory.***

## Reproducibility 
The results in the paper are not reproducible using the redacted dataset.
Most of the figures/tables in the paper and those using the reduced dataset will be different (or unproducible)
because the persistent identifiers are redacted; you may not count the number of devices or users anymore.
Also, you may not join across multiple tables.
If you want to fully reproduce the results, you must seek IRB approval and run the analysis on the full dataset.

### Citation
If you use our code or any intermediate data, please cite our paper:

```azure
@article{jakarai2024,
		author  = {Md Jakaria and
		           Danny Yuxing Huang and
                   Anupam Das},
		title   = {Connecting the Dots: Tracing Data Endpoints in IoT Devices},
		journal = {Proceedings on Privacy Enhancing Technologies (PoPETs)},
		year    = {2024},
		volume  = {2024},
		number  = {3},
	}
```