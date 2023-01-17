# aiohttp web scraper
### Disclaimer
Always take the robots.txt file of the site you are scraping into consideration and 
comply to (copyright) laws!

### Use case
1. Scrape links and titles from an index site
2. Scrape content from each link
3. Write result to a mysql database

### Usage
Adjust the config.py set the sql configuration and the sql statement to your database/table, 
set `INDEX_SITE` and `get_title_and_subpage_url()`. 
Then adjust the `get_title_and_subpage_url()` and `get_content()` functions 
to select the elements containing subpages and the content of the subpage you want to scrape.

### Why asyncio and aiohttp instead of requests or httpx?
Python asyncio and its http client aiohttp were specifically designed to concurrently run input/output bound tasks
as http requests. 
Therefore, it performs significantly better than the AsyncClient of HTTPX according to 
https://github.com/encode/httpx/issues/838.
Synchronous http libraries like requests or pycurl using threading or multiprocessing will always lose out against
asyncio for input bound tasks (https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python).

### Additional considerations
Some sites may require you to have some specific cookies or headers(especially browser-like User-Agent) set 
in order to accept the request. Adjust the according config settings if needed
