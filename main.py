from fastapi import FastAPI
from pipeline import run_research_pipeline
from models import ResearchRequest
import re

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/research")
def research(data: ResearchRequest):

    topic = data.topic
    result = run_research_pipeline(topic)

    # extract clean URLs using regex
    raw = result.get("search_results", "")
    sources = re.findall(r'https?://[^\s\)\]\,\"\'<>]+', raw)
    # deduplicate while preserving order
    seen = set()
    clean_sources = []
    for url in sources:
        url = url.rstrip(".,;:")
        if url not in seen:
            seen.add(url)
            clean_sources.append(url)

    return {
        "topic": data.topic,
        "report": {"content": result["report"]},
        "feedback": {"content": result["feedback"]},
        "sources": clean_sources
    }