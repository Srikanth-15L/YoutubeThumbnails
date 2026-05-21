from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()
def web_search(query:str) -> str:
    results=TavilyClient().search(query,max_results=5)["results"]
    return "\n".join(f"-{re['title']}:{re['content'][:200]} "for re in results)
