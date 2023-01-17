import bs4
from bs4 import BeautifulSoup


# DB config
USE_DB = False
DB_HOST = "localhost"
DB_DB = "db_name"
DB_USER = "root"
DB_PASS = ""
INSERT_STMT = "INSERT IGNORE INTO `scrape` (`id`, `subpage`, `content`) VALUES (NULL, %s, %s);"


# Scrape config
INDEX_URL = "https://lite.duckduckgo.com/lite/?q=hello+world"  # Site that contains all subpages
SUBPAGE_ELEMENT_SELECTOR = ".result-link"  # Selector that gets Elements that contain the link to the Subpage.
# get_title_and_subpage_url will be called for each result


# hardcode index term selector
def get_title_and_subpage_url(el: bs4.Tag):
    title = el.text
    subpage_url = el.attrs["href"]  # make sure to take relative urls (e.g. //content/hw.html) into consideration:
    # they need you to prepend the baseURL
    return title, subpage_url


def get_content(content: bs4.Tag) -> str:
    res = content.select("img")
    return str(len(res))


# Some sites won't redirect via HTTP but use a <meta> HTML tag instead
CHECK_META_TAG_REFRESH = True

# Some sites will require you to have specific headers and cookies set to allow your request
SESSION_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
}
SESSION_COOKIES = {}

INDEX_HEADERS = {}
INDEX_COOKIES = {}

SUBPAGE_HEADERS = {}
SUBPAGE_COOKIES = {}
