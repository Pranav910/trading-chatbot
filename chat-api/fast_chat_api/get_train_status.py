from crawl4ai import AsyncWebCrawler
import asyncio

async def scrap_train_status(url):

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

    return result.markdown

async def get_train_status(urls):

    tasks = [scrap_train_status(url) for url in urls]
    result = await asyncio.gather(*tasks)
    
    return result