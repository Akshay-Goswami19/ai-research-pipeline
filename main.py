from fastapi import FastAPI
from pipeline import run_research_pipeline
from models import ResearchRequest
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/research")
def research(data: ResearchRequest):

    topic = data.topic
    result = run_research_pipeline(topic)

    #extracting sources
    sources = []
    lines = result["search_results"].split("\n")
    for line in lines:
        if "http" in line:
            sources.append(line.replace("Url:", "").strip())

    return {
        "topic" : data.topic,
        "report" :  {"content" : result["report"]},
        "feedback" : {"content" : result["feedback"]},
        "sources" : sources
    }