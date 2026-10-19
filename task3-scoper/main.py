"""
FastAPI Server for Task 3 — Meeting to Scope.
Runs the Multi-Agent team, checks Task 1 Brain API, and renders interactive Scoping UI.
Runs on Port 8003.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from scoper_engine import scoper_instance

app = FastAPI(
    title="Meeting to Scope Multi-Agent System (Task 3)",
    version="1.0.0",
    description="Multi-agent team that turns client meetings into SOW, task estimates, and proposals with Task 1 Knowledge Brain feasibility checking."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScopeSingleRequest(BaseModel):
    transcript_filename: str
    client_name: str

class ScopeDiffRequest(BaseModel):
    transcript_1: str
    transcript_2: str
    client_name: str

class ApprovalRequest(BaseModel):
    proposal_text: str
    reviewer_name: str = "Lead AI Tech Consultant"


@app.get("/api/health")
def health():
    return {
        "service": "Task 3 — Meeting to Scope",
        "status": "healthy",
        "agents": ["Discovery Analyst", "Feasibility Architect", "Estimator & SOW Author", "Scope-Diff Agent"]
    }


@app.get("/api/transcripts")
def list_transcripts():
    transcripts_dir = os.path.join(os.path.dirname(__file__), "transcripts")
    files = [f for f in os.listdir(transcripts_dir) if f.endswith(".md")]
    return [
        {
            "filename": f,
            "title": f.replace("_", " ").replace(".md", "").title(),
            "path": f
        }
        for f in files
    ]


@app.get("/api/transcripts/{filename}")
def get_transcript(filename: str):
    try:
        content = scoper_instance.load_transcript(filename)
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/scope/single")
def run_single_scoping(req: ScopeSingleRequest):
    """Runs Discovery -> Feasibility with Task 1 Brain -> SOW & Tasks."""
    content = scoper_instance.load_transcript(req.transcript_filename)
    raw_reqs = scoper_instance.agent_discovery(content)
    evaluated = scoper_instance.agent_feasibility(raw_reqs)
    sow = scoper_instance.agent_sow(evaluated, req.client_name)
    proposal = scoper_instance.generate_full_proposal(sow)
    return {
        "client_name": req.client_name,
        "requirements_extracted": evaluated,
        "sow": sow,
        "proposal_markdown": proposal,
        "status": "PENDING_HUMAN_APPROVAL"
    }


@app.post("/api/scope/diff")
def run_scope_diff(req: ScopeDiffRequest):
    """Runs Meeting 1 vs Meeting 2 diff analysis showing additions, deletions, and cost delta."""
    m1_content = scoper_instance.load_transcript(req.transcript_1)
    m2_content = scoper_instance.load_transcript(req.transcript_2)

    m1_reqs = scoper_instance.agent_feasibility(scoper_instance.agent_discovery(m1_content))
    m2_reqs = scoper_instance.agent_feasibility(scoper_instance.agent_discovery(m2_content))

    diff = scoper_instance.agent_scope_diff(m1_reqs, m2_reqs)
    sow_revised = scoper_instance.agent_sow(m2_reqs, req.client_name)
    proposal_revised = scoper_instance.generate_full_proposal(sow_revised, scope_diff=diff)

    return {
        "client_name": req.client_name,
        "scope_diff": diff,
        "revised_sow": sow_revised,
        "proposal_markdown": proposal_revised,
        "status": "PENDING_HUMAN_APPROVAL"
    }


@app.post("/api/proposal/approve")
def approve_proposal(req: ApprovalRequest):
    """Human approval gate before proposal can be released to client."""
    return {
        "status": "APPROVED_FOR_CLIENT",
        "reviewer": req.reviewer_name,
        "message": "Proposal and SOW formally approved by senior consultant. Ready for client delivery.",
        "proposal": req.proposal_text
    }


static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Task 3 Scoper API Running</h1>")


if __name__ == "__main__":
    import uvicorn
    print("\n -> Task 3 Scoper Dashboard: http://localhost:8003\n -> Swagger API Docs:      http://localhost:8003/docs\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=False)
