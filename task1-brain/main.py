"""
FastAPI REST Server for Task 1 — The Knowledge Brain.
Exposes clean, documented APIs for Tasks 2 and 3, plus an interactive web UI.
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

from brain_engine import brain_instance
from crawler import PoliteBrainCrawler

app = FastAPI(
    title="Knowledge Brain API — Brilliant Directories Solution Center",
    version="1.0.0",
    description="Single source of truth knowledge brain with multimodal screenshot context, polite crawler, and self-improving escalation feedback loop."
)

# Enable CORS for Tasks 2 and 3
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crawler_instance = PoliteBrainCrawler(polite_delay_sec=0.5)

# Pydantic schemas
class SearchRequest(BaseModel):
    query: str = Field(..., example="How do I connect Stripe payment gateway?")
    top_k: int = Field(default=5, ge=1, le=20)

class ChatRequest(BaseModel):
    query: str = Field(..., example="Can I give a refund to a cancelled member?")

class CapabilityRequest(BaseModel):
    feature_description: str = Field(..., example="Add Facebook and Twitter profile icons to the header and footer")

class ResolveEscalationRequest(BaseModel):
    answer: str = Field(..., min_length=10, example="You can issue a full or partial refund in Finance >> Transaction History.")
    expert_name: str = Field(default="Senior Tech Consultant")

class SyncRequest(BaseModel):
    max_articles: int = Field(default=5, ge=1, le=50)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Task 1 — Knowledge Brain",
        "total_articles": len(brain_instance.articles),
        "custom_knowledge_items": len(brain_instance.custom_knowledge),
        "pending_escalations": len([e for e in brain_instance.escalations if e["status"] == "pending"]),
        "total_escalations": len(brain_instance.escalations)
    }


@app.get("/api/sitemap/status")
def get_sitemap_status():
    """Get the latest daily freshness status between local brain and live sitemap."""
    return crawler_instance.check_freshness()


@app.post("/api/sitemap/sync")
def trigger_sitemap_sync(req: SyncRequest):
    """Trigger polite crawler to fetch fresh articles in batches."""
    scraped_count = crawler_instance.scrape_articles_polite(max_articles=req.max_articles)
    brain_instance.reload_all()
    return {
        "status": "success",
        "scraped_count": scraped_count,
        "total_articles_now": len(brain_instance.articles)
    }


@app.get("/api/articles")
def list_articles(category: Optional[str] = None, q: Optional[str] = None, limit: int = 20):
    """List indexed knowledge articles with optional category or keyword filter."""
    articles = list(brain_instance.articles.values()) + list(brain_instance.custom_knowledge.values())
    if category:
        articles = [a for a in articles if a.get("category", "").lower() == category.lower()]
    if q:
        search_res = brain_instance.search(q, top_k=limit)
        return [r["article"] for r in search_res]
    return articles[:limit]


@app.get("/api/articles/{article_id}")
def get_article(article_id: str):
    """Retrieve full article by ID with multimodal screenshot descriptions."""
    if article_id in brain_instance.articles:
        return brain_instance.articles[article_id]
    if article_id in brain_instance.custom_knowledge:
        return brain_instance.custom_knowledge[article_id]
    raise HTTPException(status_code=404, detail="Article not found in knowledge brain.")


@app.post("/api/search")
def search_knowledge(req: SearchRequest):
    """Hybrid search returning ranked articles, score, and image context."""
    return brain_instance.search(req.query, top_k=req.top_k)


@app.post("/api/chat")
def chat_with_brain(req: ChatRequest):
    """
    Primary Q&A endpoint:
    Returns factual answer, confidence, cited source articles, and honest abstention if unknown.
    """
    return brain_instance.answer_query(req.query)


@app.post("/api/capability-check")
def check_capability_endpoint(req: CapabilityRequest):
    """
    Endpoint for Tasks 2 & 3:
    Checks if a client feature request is a native setting, standard customization, or custom dev.
    """
    return brain_instance.check_capability(req.feature_description)


@app.get("/api/escalations")
def list_escalations(status: Optional[str] = None):
    """List human expert escalation queue."""
    if status:
        return [e for e in brain_instance.escalations if e.get("status") == status]
    return brain_instance.escalations


@app.post("/api/escalations/{escalation_id}/resolve")
def resolve_escalation_endpoint(escalation_id: str, req: ResolveEscalationRequest):
    """
    Resolve escalation and feed verified answer back into the Knowledge Brain memory.
    """
    result = brain_instance.resolve_escalation(escalation_id, req.answer, req.expert_name)
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result


# Mount static directory for UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Knowledge Brain API is running</h1><p>Visit <a href='/docs'>/docs</a> for Swagger API.</p>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
