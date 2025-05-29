import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import concurrent.futures
from tldextract import extract
import requests
from serpapi import GoogleSearch

def crawl(query, max_results=5):

    # search_url = 'https://html.duckduckgo.com/html/'
    # params = {'q': query}
    # headers = {'User-Agent': 'Mozilla/5.0'}

    # favicon_links = []

    # response = requests.post(search_url, data=params, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')

    # links = []
    # for a in soup.find_all('a', attrs={'class': 'result__a'}):
    #     t = extract(a['href'])
    #     domain = f"https://www.{t.domain}.{t.suffix}"
    #     favicon_links.append(domain + "/favicon.ico")
    #     links.append(a['href'])
    #     if len(links) >= max_results:
    #         break

    # return links, favicon_links

    search_result = GoogleSearch({
        "q": query,
        "api_key": "a14ab0e0525df8fd7ce55d9ecc4bdf861cc95ab4404066531b0d8501b4975d48",
        "engine": "google",
        "num": 5
    })

    links = []
    favicon_links = []

    for result in search_result.get_dict().get("organic_results", []):
        url = result.get("link")
        t = extract(url)
        domain = f"https://www.{t.domain}.{t.suffix}"
        favicon_links.append(domain + "/favicon.ico")
        if url:
            links.append(url)
        if len(links) >= max_results:
            break

    return links, favicon_links


def scrap(url):

    try:
        loader = WebBaseLoader(url)
        result = loader.load()

        if result[0].metadata.get("title") == "Access Denied":
            return ""

        result = " ".join(result[0].page_content.split())

        return result
    except:
        return ""


def load_results_concurrently(urls):

    urls.append("https://www.aljazeer/")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(scrap, urls))
    
# sources = [
#         "https://cricket.one/cricket-news/yesterdays-ipl-match-result-who-won-yesterday-lsg-vs-srh-ipl-2025/682bb46c9724cd66d538fdde",
#         "https://www.espncricinfo.com/series/ipl-2025-1449924/lucknow-super-giants-vs-sunrisers-hyderabad-61st-match-1473499/live-cricket-score?ex_cid=inshorts",
#         "https://www.ascores.com/cricket-news/who-won-yesterdays-ipl-2025-match-lsg-vs-srh-61st-match-result-full-scorecard",
#         "https://www.firstpost.com/firstcricket/lsg-vs-srh-live-score-2025-ipl-match-61-live-cricket-score-updates-lucknow-super-giants-vs-sunrisers-hyderabad-full-scorecard-ekana-stadium-rishabh-pant-pat-cummins-liveblog-13889789.html",
#         "https://www.sportskeeda.com/cricket/news-lsg-vs-srh-19-5-who-won-yesterday-s-ipl-2025-match",
#         "https://www.aljazeer/"
#     ]

# result = []

# try:

#     for source in sources:
#         loader = WebBaseLoader(source)
#         result = loader.load()
#         if result[0].metadata.get("title") != "Access Denied":
#             print(result[0])
# except:

#     print("Some error occured")