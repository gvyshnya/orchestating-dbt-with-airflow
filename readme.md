# ДЗ 05 "Соцмережі та медіапростір: збір, моніторинг, базовий аналіз"

## Basic Level

The purpose of this activity was to build a basic Web data scrapper / HTML parser using Crawl4AI[https://docs.crawl4ai.com/] technology.

The flow of the basic-level scrapper was as follows

- navigate to https://www.crugroup.com/en/commodities/
- scrap no more then 10 pages linked from the above-mentioned URL, using the Deep Crawling BFS strategy (*BFSDeepCrawlStrategy* in *Crawl4AI*, with max 10 pages and max depth of nested page scan to be 2)
- save the raw html content of the srapped webpages to [./data/raw] subfolder
- extract the essencial details about each page scrapped as a normilized JSON data structure
- save the normalized JSON data for each of the pages scrapped to [./data/normalized] subfolder

The normalized JSON data structure will contain the following attributes for each of the pages scrapped
- url
- title
- fetched_at
- source
- content
- links

**Note:** Only 500 initial characters of the page content (cleaned from HTML into markdown) have been extracted into JSON *content* attribute.

The artifacts below demonstrate the implementation of the basic web crawler

- Source code: [crawler_1/crawler1.py]
- Screenshot to demonstrate the parser execution: [screenshots/crawler_1_running.png]
- Example output of the raw HTML data: [crawler_1/data/raw] subfolder
- Example output of the normalized JSON data: [crawler_1/data/normalized] subfolder

### Technical Implementation Notes

The basic crawler utilized one of the simple crawling strategies (that is, a basic Deep Crawling with BFS strategy). It was more then enough for the basic task being solved here.

More sophisticated deep crawling strategies () as well as advanced adaptive crawling strategies are not required for this task. Such complex crawling strategies are used in more complex use cases when

- you need to collect the data from dynamic web sites (with the content decorated in certain CSS rules or produced dynamically by JS on the browser client side)
- you need to summarize/interprete your scrapped data with LLM/AI models
- you have to implement more sophisticated scenarios that require adaptive crawling [https://docs.crawl4ai.com/core/adaptive-crawling/]

## Advanced Level

The purpose of this activity was to build a more advanced Web data scrapper using Crawl4AI[https://docs.crawl4ai.com/] technology. More specifically, the goal was to build a pipeline to collect the pricing details about OpenAI model API pricing in a scructured way.

The flow of the basic-level scrapper was as follows

- navigate to [https://openai.com/api/pricing/]
- extract pricing information for every model/API Access level listed there, using *JsonCssExtractionStrategy* and the page-specific CSS schema of the pricing data representation on that page
- output the collected information as a well-formed structured JSON file 

The artifacts below demonstrate the implementation of the advanced web crawler

- Source code: [crawler_2/crawler2.py]
- Screenshot to demonstrate the parser execution: [screenshots/crawler_2_running.png]
- JSON output of the collected pricing data: [crawler_2/data/pricing.json]

## Trial of LLMExtraction Crawling strategies

I tried to code the web crawler with LLMExtraction strategies [https://docs.crawl4ai.com/extraction/llm-strategies/]. However, it did not fly quickly. I need more time to implement it properly (outside the scope of the current homework assignment).

## Used Instruments and Dependencies

Crawl4AI[https://docs.crawl4ai.com/], the Open-Source LLM-Friendly Web Crawler & Scraper (v. 0.8.6), has been used as a technical platform to implement both the web scrappers of the basic and advanced levels.

Crawl4AI capabilities have been leveregad via the customly developed Python scripts. 

Standard Python libraries have been used to implement JSON processing and logging (*json* and *logging*, respectively).

Python scripts have been deployed into the Dockerized Crawl4AI server instances spinned with the crawl4ai Docker image (as explained in [https://github.com/unclecode/crawl4ai]).

**Note:** Using Crawl4AI-provided Docker image eliminated the need to build the own custom Docker image for our html workers (therefore, they are not the part of the submission).


## Known Issues

1/ Crawl4ai could not be installed on Python 3.14 runtime due to https://github.com/unclecode/crawl4ai/issues/1903 - I had to downgrade python in the target conda environment to 3.13

2/ Crawl4ai eventually installed on python 3.13 but the healthcheck failed:

```Test failed: BrowserType.launch: Executable doesn't exist at
C:\Users\***\AppData\Local\ms-playwright\chromium-1217\chrome-win64\chrome.exe```

Workaround: run the command below in the target conda environment:
```python -m playwright install --with-deps chromium```

described in more details in https://github.com/unclecode/crawl4ai/issues/503

After it, the healthcheck was successful
```>> crawl4ai-doctor```

## Files and Folders

- readme.md - this readme document
- [crawler_1] subfolder contains the artifacts related to the basic crawler task (see explanations above)
- [crawler_2] subfolder contains the artifacts related to the advanced crawler task (see explanation above)
- [screenshots] subfolder contains essential screenshots that illustrate essential details about implementation of the basic and advanced crawlers