# Data Collection - Phase 1

In this phase2, the initial dataset is constructed from the following data sources:

<em>The following data resources have been scraped:</em>
* `https://discourse.ros.org/` <em>(crawled on: February 21-22)</em>
* `https://stackoverflow.com/questions/tagged/ros`<em>(crawled on: February 17)</em>
* `https://answers.ros.org/questions/`<em>(crawled on: February 17)</em>
* `GitHub, BitBucket` <em>(Git/BitBucket Issues/PRs crawled on: February 25 - March 1. Src comments/.md files crawled on: February 24)</em>
    * Identified `ROS` repositories found in: `phase1_data_collection/git_scraper/Repos_all.csv`

**Requirements**

`python 3.x.x`

`scrapy`

**Run spiders**

`cd phase1_data_collection/*WebCrawler/*WebCrawler/spiders`

<em>Test/run output</em>

`scrapy crawl <spider_name> --nolog`

<em>Start crawling</em>

`scrapy crawl <spider_name> -o /path/to/data/storage/data.json -t json`

**Run git data extractor**

<em>`git_data_extractor.py` extracts `c++` and `python` source code comments and `.md` contents for each repository.</em>

`cd phase1_data_collection/git_scraper`

<em>Generate data</em>

`python3 git_data_extractor.py`

Generated data found in: `phase1_data_collection/git_scraper/data`

## Energy Detector - Phase 2

In this phase, the dataset from **Phase 1** is queried to filter out **energy-related** data.

**Run Energy Detectors**

`cd phase2_energy_detector/energy_detectors`

`python3 energy_detector_<data_source_name>.py`

**Write data to CSV**

`cd phase2_energy_detector/energy_to_csv`

`python3 <data_source_name>_energy_to_csv.py`

The energy CSV spreadsheets are found in: `phase2_energy_detector/energy_to_csv/data`

The energy data dump can be found in: `phase2_energy_detector/energy_data_dump.xlsx`

## SA-Energy Detector - Phase 3
