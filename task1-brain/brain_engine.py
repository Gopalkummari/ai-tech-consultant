"""
Knowledge Brain Engine: Hybrid Retrieval, Capability Checker, Source-Cited RAG,
and Human Escalation Feedback Loop.
"""

import os
import json
import math
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrainEngine")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")
ESCALATIONS_FILE = os.path.join(DATA_DIR, "escalations.json")
CUSTOM_KNOWLEDGE_FILE = os.path.join(DATA_DIR, "custom_knowledge.json")


class BrainEngine:
    def __init__(self):
        self.articles: Dict[str, Dict[str, Any]] = {}
        self.custom_knowledge: Dict[str, Dict[str, Any]] = {}
        self.escalations: List[Dict[str, Any]] = []
        self.reload_all()

    def reload_all(self):
        """Reload articles, custom knowledge, and escalations from disk."""
        if os.path.exists(ARTICLES_FILE):
            with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
                self.articles = {a["id"]: a for a in json.load(f)}

        if os.path.exists(CUSTOM_KNOWLEDGE_FILE):
            with open(CUSTOM_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                self.custom_knowledge = {k["id"]: k for k in json.load(f)}
        else:
            self.custom_knowledge = {}

        if os.path.exists(ESCALATIONS_FILE):
            with open(ESCALATIONS_FILE, "r", encoding="utf-8") as f:
                self.escalations = json.load(f)
        else:
            self.escalations = []

    def _save_escalations(self):
        with open(ESCALATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.escalations, f, indent=2)

    def _save_custom_knowledge(self):
        with open(CUSTOM_KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(self.custom_knowledge.values()), f, indent=2)

    def _tokenize(self, text: str) -> List[str]:
        cleaned = "".join([c.lower() if c.isalnum() else " " for c in text])
        return [w for w in cleaned.split() if len(w) > 2]

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Hybrid search combining keyword BM25/TF-IDF and tag/title weighting
        across articles and multimodal image descriptions.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        all_docs = list(self.articles.values()) + list(self.custom_knowledge.values())
        scores = []

        for doc in all_docs:
            title_text = doc.get("title", "")
            content_text = doc.get("content", "")
            tags = " ".join(doc.get("tags", []))
            image_descs = " ".join([img.get("vision_description", "") + " " + img.get("alt", "") for img in doc.get("images", [])])

            title_tokens = self._tokenize(title_text)
            content_tokens = self._tokenize(content_text)
            tag_tokens = self._tokenize(tags)
            image_tokens = self._tokenize(image_descs)

            score = 0.0
            matched_terms = []

            for qt in query_tokens:
                # Title matches (weight 4.0)
                if qt in title_tokens:
                    score += 4.0
                    matched_terms.append(qt)
                # Tag matches (weight 3.0)
                if qt in tag_tokens:
                    score += 3.0
                    matched_terms.append(qt)
                # Content match frequency (weight 1.0)
                c_count = content_tokens.count(qt)
                if c_count > 0:
                    score += 1.0 + math.log(1 + c_count)
                    matched_terms.append(qt)
                # Image description match (weight 2.5) - multimodal evidence
                img_count = image_tokens.count(qt)
                if img_count > 0:
                    score += 2.5 + math.log(1 + img_count)
                    matched_terms.append(f"image:{qt}")

            if score > 0:
                normalized_score = min(1.0, score / (len(query_tokens) * 4.5))
                scores.append({
                    "score": round(normalized_score, 3),
                    "article": doc,
                    "matched_terms": list(set(matched_terms)),
                    "has_multimodal_match": any("image:" in m for m in matched_terms)
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    def answer_query(self, query: str) -> Dict[str, Any]:
        """
        Chatbot QA pipeline:
        - Retrieves top matching articles and multimodal screenshot context.
        - Provides direct factual answers with exact citations.
        - Honestly abstains and generates an escalation when confidence < 0.35.
        """
        search_results = self.search(query, top_k=3)
        top_match = search_results[0] if search_results else None
        confidence = top_match["score"] if top_match else 0.0

        if not top_match or confidence < 0.35:
            # Escalation triggered
            escalation_id = f"esc-{int(datetime.now().timestamp()*1000)}"
            escalation_entry = {
                "id": escalation_id,
                "query": query,
                "confidence": confidence,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "pending",
                "resolved_answer": None,
                "resolved_at": None,
                "resolved_by": None
            }
            self.escalations.insert(0, escalation_entry)
            self._save_escalations()

            return {
                "answer": "I do not have enough verified documentation in the Brilliant Directories Knowledge Brain to answer this question accurately. I have created an escalation ticket for a technical consultant to review and resolve.",
                "confidence": confidence,
                "sources": [],
                "escalated": True,
                "escalation_id": escalation_id,
                "honest_abstention": True
            }

        # Build answer synthesized from the top cited article(s)
        best_doc = top_match["article"]
        answer_text = self._synthesize_answer(query, best_doc, search_results)

        sources = []
        for r in search_results[:2]:
            doc = r["article"]
            sources.append({
                "id": doc.get("id"),
                "title": doc.get("title"),
                "url": doc.get("url"),
                "category": doc.get("category"),
                "folder": doc.get("folder"),
                "relevance_score": r["score"],
                "images": doc.get("images", [])
            })

        return {
            "answer": answer_text,
            "confidence": confidence,
            "sources": sources,
            "escalated": False,
            "escalation_id": None,
            "honest_abstention": False
        }

    def _synthesize_answer(self, query: str, doc: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
        """Synthesize answer citing specific settings and multimodal screenshot insights."""
        title = doc.get("title", "")
        content = doc.get("content", "")
        category = doc.get("category", "")
        folder = doc.get("folder", "")
        images = doc.get("images", [])

        # Extract primary lines
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        core_steps = [l for l in lines if l[0].isdigit() or "Steps" in l or "Settings" in l][:4]
        steps_summary = "\n".join(core_steps) if core_steps else lines[:3]

        img_context = ""
        if images:
            img = images[0]
            img_context = f"\n\nVisual Context (Screenshot): {img.get('vision_description')}"

        return (
            f"Based on Brilliant Directories Solution Center documentation ({category} > {folder}):\n\n"
            f"{content[:350]}...\n\n"
            f"Key configuration path:\n{steps_summary}"
            f"{img_context}"
        )

    def check_capability(self, feature_description: str) -> Dict[str, Any]:
        """
        Feasibility & Native Setting Checker used by Task 2 & Task 3:
        Determines whether a requested client feature is:
        - 'NATIVE_SETTING' (built-in configuration toggle, $0 dev cost)
        - 'STANDARD_CUSTOMIZATION' (forms, widget overrides, CSS)
        - 'COMPLEX_CUSTOM_DEV' (external backend, complex custom logic)
        """
        results = self.search(feature_description, top_k=3)
        top = results[0] if results else None

        if top and top["score"] >= 0.50:
            doc = top["article"]
            content_lower = doc.get("content", "").lower()
            title_lower = doc.get("title", "").lower()

            if "native setting" in content_lower or "100% built-in" in content_lower or "settings >>" in content_lower:
                return {
                    "classification": "NATIVE_SETTING",
                    "confidence": top["score"],
                    "is_native": True,
                    "setting_location": self._extract_setting_path(doc["content"]),
                    "recommended_action": "Use built-in settings toggle in admin panel. Do NOT quote custom coding.",
                    "estimated_hours": 0.5,
                    "cost_to_client": 50.0,
                    "savings_vs_custom": 1500.0,
                    "source_article": {
                        "id": doc["id"],
                        "title": doc["title"],
                        "url": doc["url"]
                    }
                }
            elif "form manager" in content_lower or "widget manager" in content_lower or "custom css" in content_lower:
                return {
                    "classification": "STANDARD_CUSTOMIZATION",
                    "confidence": top["score"],
                    "is_native": False,
                    "setting_location": "Toolbox >> Form Manager or Widget Manager",
                    "recommended_action": "Configure via Form Manager or Bootstrap Theme Widget override.",
                    "estimated_hours": 3.0,
                    "cost_to_client": 300.0,
                    "savings_vs_custom": 1000.0,
                    "source_article": {
                        "id": doc["id"],
                        "title": doc["title"],
                        "url": doc["url"]
                    }
                }

        # Out-of-the-box or complex custom dev
        return {
            "classification": "COMPLEX_CUSTOM_DEV",
            "confidence": top["score"] if top else 0.1,
            "is_native": False,
            "setting_location": "Requires custom webhook/API development or external microservice.",
            "recommended_action": "Scope as custom engineering project with API integration.",
            "estimated_hours": 20.0,
            "cost_to_client": 2000.0,
            "savings_vs_custom": 0.0,
            "source_article": None
        }

    def _extract_setting_path(self, text: str) -> str:
        for line in text.split("\n"):
            if ">>" in line or "Settings >" in line:
                return line.strip()
        return "Admin Dashboard >> Settings"

    def resolve_escalation(self, escalation_id: str, expert_answer: str, expert_name: str = "Senior Consultant") -> Dict[str, Any]:
        """
        Self-evolving loop:
        When human expert resolves a pending question, store the resolution and
        ingest it back into the Knowledge Brain as an approved knowledge item!
        """
        target = None
        for esc in self.escalations:
            if esc["id"] == escalation_id:
                target = esc
                break

        if not target:
            return {"status": "error", "message": f"Escalation {escalation_id} not found."}

        target["status"] = "resolved"
        target["resolved_answer"] = expert_answer
        target["resolved_at"] = datetime.now(timezone.utc).isoformat()
        target["resolved_by"] = expert_name
        self._save_escalations()

        # Ingest into custom knowledge brain
        custom_id = f"custom-{escalation_id}"
        self.custom_knowledge[custom_id] = {
            "id": custom_id,
            "url": f"internal://escalations/{escalation_id}",
            "title": f"Verified Solution: {target['query']}",
            "category": "Expert Verified Knowledge",
            "folder": "Human-in-the-Loop Solutions",
            "last_modified": target["resolved_at"],
            "content": f"Query: {target['query']}\n\nExpert Verified Solution:\n{expert_answer}\n\nResolved by: {expert_name}",
            "images": [],
            "tags": ["expert-verified", "escalation-resolved"] + [w.lower() for w in target['query'].split() if len(w) > 3]
        }
        self._save_custom_knowledge()
        logger.info(f"Ingested verified answer {custom_id} into Brain Memory.")

        return {
            "status": "success",
            "escalation": target,
            "knowledge_item_id": custom_id
        }


brain_instance = BrainEngine()
