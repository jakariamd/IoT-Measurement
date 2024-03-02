This directory includes scripts to collect data for endpoint mappings. These files are related to Section 5 of the paper.

| File/Directory Name            | Description                                                                                                                 |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| First Party Mapping            | Contains scripts  to collect data from different sources for first party mapping (Section 5.1 of the paper)                 |
| Support Party Mapping          | Contains scripts to collect data and build topic models for support party mapping (Section 5.2 of the paper)                |
| Endpoint Mapping with LLM      | Contains scripts to validate design choice of Endpoint mapping (Section 5.4)                                                | 
| Clean Network Flow.ipynb       | Clean clean network flow statistics, removes local/DNS/NTP communications/ extracts eTLD+1 or hostnames of remote endpoints | 
| Mapping First Party.ipynb      | Maps first party domains to vendors using data collected from different sources                                             | 
| Mapping Support Parties .ipynb | Maps support party domains to vendors using topic models                                                                    |

Run the script in the following order:

1. Run ``Clean Network Flow.ipynb`` to get unique remote host names 
2. Run scripts in ***First Party Mapping*** directory to collect data related to first party
3. Run ```Mapping First Party.ipynb ``` to get first party vendor-domains
4. Run scripts in ***Support Party Mapping*** directory and ```Mapping Support Parties .ipynb``` to collect data and get support party vendor-domains

To run scripts
```bash
cd <code directory>
jupyter nbconvert --execute --to html --no-input <script-name>"
```
