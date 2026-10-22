"""AeroThermal RAG Engine: Grounded Retrieval-Augmented Generation for Disaster Resilience.
Integrates statutory NADMA Directive 20, JPS MSMA hydrology, and JKM PPS standards with
City of Elmina live catchment telemetry.
"""
import json
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)

CORPUS_PATH = Path(__file__).resolve().parent / "knowledge" / "corpus.json"
_CHUNKS = None

STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with', 'what', 'where', 'when', 'who', 'how', 'which', 'our', 'we',
    'can', 'you', 'your', 'i', 'me', 'my', 'do', 'does', 'if', 'this', 'there'
}


def load_corpus():
    global _CHUNKS
    if _CHUNKS is None:
        try:
            with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
                _CHUNKS = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load RAG corpus from {CORPUS_PATH}: {e}")
            _CHUNKS = []
    return _CHUNKS


def tokenize(text):
    words = re.findall(r'\b[a-z0-9%_\-]+\b', text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def retrieve(query_text, top_k=2):
    """Retrieve top-K authoritative statutory chunks matching query using BM25-style lexical scoring."""
    corpus = load_corpus()
    tokens = tokenize(query_text)
    if not tokens:
        return []

    scored_chunks = []
    for chunk in corpus:
        score = 0.0
        chunk_keywords = set(k.lower() for k in chunk.get('keywords', []))
        chunk_title_tokens = set(tokenize(chunk.get('title', '')))
        chunk_text_lower = chunk.get('text', '').lower()

        for t in tokens:
            # High weight for keyword tag match
            if t in chunk_keywords:
                score += 4.0
            # Medium weight for title token match
            if t in chunk_title_tokens:
                score += 3.0
            # Term occurrences in body text
            count = chunk_text_lower.count(t)
            if count > 0:
                score += min(count, 3) * 1.0

        if score > 0:
            scored_chunks.append({
                'chunk_id': chunk['id'],
                'source': chunk['source'],
                'clause': chunk['clause'],
                'title': chunk['title'],
                'text': chunk['text'],
                'score': round(score, 2),
            })

    # Sort descending by relevance score
    scored_chunks.sort(key=lambda x: x['score'], reverse=True)
    return scored_chunks[:top_k]


def build_rag_system_prompt(telemetry, retrieved_chunks):
    """Construct a strictly grounded RAG system instruction for LLM inference."""
    # Build retrieved knowledge passage block
    if retrieved_chunks:
        docs_text = "\n\n".join(
            f"[{idx+1}] {c['source']} ({c['clause']})\nTITLE: {c['title']}\nEXCERPT: {c['text']}"
            for idx, c in enumerate(retrieved_chunks)
        )
    else:
        docs_text = "No direct statutory document matched. Rely on core Sime Darby Elmina Catchment Engineering baseline."

    mode_label = telemetry.get('mode', 'normal').title()
    stored_m3 = telemetry.get('stored_m3', 65000)
    capacity_m3 = telemetry.get('capacity_m3', 100000)
    lake_pct = telemetry.get('lake_pct', 65.0)
    buffer_m3 = telemetry.get('buffer_m3', 35000)
    active_reports = telemetry.get('active_reports', 0)

    prompt = f"""You are AeroThermal AI, the official Disaster Resilience Copilot for Sime Darby Property's City of Elmina township.
Your advice is strictly grounded in official statutory frameworks from NADMA Malaysia, JPS Selangor, and JKM.

GROUNDING FACTS & CURRENT CATCHMENT TELEMETRY:
- Always answer in 100% professional English.
- Active Scenario: {mode_label}
- Retention Basin Level: {lake_pct}% ({stored_m3:,} m³ stored of {capacity_m3:,} m³ total capacity)
- Available Retention Buffer: {buffer_m3:,} m³
- Active Field Reports: {active_reports} reports logged by township operations
- Evacuation Shelters: Elmina Central Community Hall (1,200 pax capacity, 150 kVA generator, 10,000L water tank)
- Emergency Corridors: Persiaran Mokhtar Dahari flyover (42m RL), CoolWalk Shaded Trail (36-39m RL)
- National Emergency Contacts: 999 (National Emergency), 994 (BOMBA), 03-8064 2400 (NADMA Command Centre)

RETRIEVED STATUTORY DOCUMENT CONTEXT (RAG):
{docs_text}

INSTRUCTIONS:
1. Ground your answer directly in the RETRIEVED STATUTORY DOCUMENT CONTEXT above.
2. Cite the retrieved source using brackets like [1] or [Source: NADMA Directive 20] when referencing regulatory requirements.
3. If the user sends a greeting (e.g. "hello", "hi"), give a warm, concise executive greeting, state your mission as AeroThermal AI Copilot, highlight the current live basin level ({lake_pct}%), and invite them to explore resilience operations.
4. If a question cannot be answered using the retrieved context or live telemetry, explicitly state that the official operational manual does not cover that specific detail.
5. Format answers cleanly with markdown headings, structured bullet points, and actionable checklists (- [ ])."""

    return prompt
