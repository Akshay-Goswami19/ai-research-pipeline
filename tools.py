from dotenv import load_dotenv
load_dotenv()

import os,requests
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
from rich import print

tavily = TavilyClient(api_key= os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs and snippets"""
    results = tavily.search(
        search_depth= "basic",
        query= query,
        max_results= 2
    )

    out = []

    for r in results["results"]:
        out.append(
            f"Title: {r["title"]} \n Url: {r["url"]}  \n Snippet {r["content"][:300]} \n"
        )
    
    return "\n-----\n".join(out)



@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    

