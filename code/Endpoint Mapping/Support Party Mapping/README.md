This directory includes a compilation of notebooks along with a utility file for mapping remote endpoints. These files pertain to Section 5.2 of the paper.

| File Name                 | Description                                                                   |
|---------------------------|-------------------------------------------------------------------------------|
| Scrape Google SERP.ipynb  | This script scrape Google SERP to extract relevant information about domains. |
| Scrape Bing SERP.ipynb    | This script scrape Bing SERP to extract relevant information about domains.   |
| Scrape Netify Pages.ipynb | This script filters domains based on their provided services.                 |
| Pre-Process Data.ipynb    | Pre-Process Data collected from Google and Bing SERP for NMF Model            |
| NMF Models.ipynb          | This script used to create NMF Topic model described in Section-5.2           |

Run all ```Scrape Bing Google.ipynb``` and ```Scrape Bing SERP.ipynb```
files to scrape metadata for given domains/endpoints 
from different sources Search Engines. We recommend to use APIs to avoid 
rate limit errors.
Preprocess collected data with ```Pre-Process Data.ipynb ``` and create 
topic models with ``NMF Models.ipynb ``.
Remember to uncomment any code line in the file (marked with ```\todo```)
to save collect data for entire domain set or to save data in file.

```bash
cd "code\Endpoint Mapping\Support Party Mapping\"
jupyter nbconvert --execute --to html --no-input <script-name>"
```