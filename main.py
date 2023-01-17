import os

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import mysql.connector

from config import *


async def write_out(term, content):
    if USE_DB:
        cursor.execute(INSERT_STMT, (term.strip(), content))
        db.commit()
    else:
        print(term.strip())
        print(content + "\n")


async def consume_site(session, term, url):
    if "https://" not in url and "http://" not in url:
        url = "http://" + url[:2].replace("//", "") + url[2:]
    try:
        res = await session.get(url)
        content = await res.text()
        soup = BeautifulSoup(content, features="html.parser")
        if CHECK_META_TAG_REFRESH:
            meta_refresh = soup.select_one("meta[http-equiv='refresh']")
            if meta_refresh is not None:
                redirect_url = meta_refresh.attrs["content"].split("=")[1]
                res = await session.get(redirect_url, headers=SUBPAGE_HEADERS, cookies=SUBPAGE_COOKIES)
                soup = BeautifulSoup(await res.text(), features="html.parser")
                content = get_content(soup)
                await write_out(term, content)
                return
        get_content(content)
        await write_out(term, content)
    except Exception as e:
        print(f"Got exception trying to scrape subpage {url}:", type(e), e)


async def main():
    session = aiohttp.ClientSession(headers=SESSION_HEADERS, cookies=SESSION_COOKIES)
    res = await session.get(INDEX_URL, headers=INDEX_HEADERS, cookies=INDEX_COOKIES)
    soup = BeautifulSoup(await res.text(), features="html.parser")
    subpage_els = soup.select(SUBPAGE_ELEMENT_SELECTOR)
    print(f"Scraped Index site, found {len(subpage_els)} elements")
    tasks = []
    for subpage_el in subpage_els:
        title, subpage_url = get_title_and_subpage_url(subpage_el)
        # term, expl_url = a.text.strip(), a.attrs["href"].strip()
        tasks.append(consume_site(session, title, subpage_url))
    await asyncio.gather(*tasks)
    await session.close()


if __name__ == '__main__':
    if USE_DB:
        db = mysql.connector.connect(host=DB_HOST,
                                     database=DB_DB,
                                     user=DB_USER,
                                     password=DB_PASS)
        cursor = db.cursor(prepared=True)
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    if USE_DB:
        db.close()
