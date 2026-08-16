# Campaign Assistant — a source-grounded RAG bot for a mayoral campaign

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

A retrieval-augmented chatbot that answers voters' questions about a candidate's policies and record — **from a curated, credibility-tracked knowledge base**, in multiple languages. Built for Mussab Ali's 2025 Jersey City mayoral campaign, with the design constraint that matters most in a political setting: it should ground answers in vetted sources and say when it isn't sure, rather than improvise.

---

## The problem

Campaigns get the same questions thousands of times, in many languages, at all hours — "what's the housing plan?", "where does the candidate stand on policing?" — and the cost of a *wrong* answer is uniquely high: a hallucinated policy position is a news story. A plain LLM is the wrong tool here precisely because it will confidently fill gaps. What a campaign needs is an assistant that answers **only from approved material**, attributes what it says, and degrades gracefully ("I don't have a verified source on that") instead of confabulating. Jersey City is also one of the most linguistically diverse cities in the US, so English-only is a non-starter.

## Market

Civic / political technology is a real and growing category — US political-tech and campaign-software spending runs into the **hundreds of millions per cycle**, and conversational constituent services are an emerging line item for both campaigns and city governments. The defensible, responsible slice is exactly the hard part here: **grounded, auditable** Q&A, as opposed to an ungoverned chatbot that becomes a liability. The same architecture generalizes directly to municipal 311-style services and any organization that must answer from an approved corpus.

## The solution

A two-stage RAG system over a governed knowledge base:

1. **Retrieve** — multi-stage matching (keyword + full-text + topic hierarchy + multilingual keyword expansion) pulls candidate facts from a structured store.
2. **Generate** — the LLM answers *from the retrieved items only*, carrying each item's **source attribution and credibility level** through to the response.

## Technical breakdown (the core)

The engineering is in the knowledge layer, not the prompt:

- **A typed, governed knowledge base** (`backend/src/knowledge_base.py`) — `KnowledgeItem`s with rich metadata (content type, topics/subtopics, keywords, confidence) backed by SQLite, and `KnowledgeSource`s carrying an explicit **`SourceCredibility`** level (Primary / Verified / Secondary / Unverified). Credibility isn't a vibe; it's a field that travels with every answer.
- **Multi-stage retrieval** — keyword and full-text matching combined with a topic hierarchy and **multilingual keyword expansion**, so a question in another language still hits the right English-sourced facts.
- **Two-step processing** — retrieval is deliberately separated from generation so the model can't answer outside the corpus; this is the architectural choice that makes the bot *safe to deploy* on a campaign.
- **Served behind a clean API** (`/api/chat`, `/api/health`, `/api/refresh-data`) with a test suite (`test_complete_system.py`) so the knowledge base can be refreshed without redeploying.

**Skills demonstrated:** RAG system design with an emphasis on groundedness and source attribution; schema design for a metadata-rich knowledge store; multilingual retrieval; API design; and — most relevant to safe AI deployment — building a system whose *architecture* prevents the failure mode (hallucinated, unsourced claims) rather than hoping a prompt will.

## Why it's relevant beyond the campaign

The hard problem here is the same one that shows up across applied AI safety: **make a capable model answer only from what it should, attribute its claims, and abstain when it can't.** This repo is a concrete, deployed instance of grounded, auditable generation — the responsible-deployment pattern, in a setting where the cost of getting it wrong is immediate and public.

## Run it

```bash
pip install -r requirements.txt
python backend/src/app.py        # serve the chat API
python test_complete_system.py   # end-to-end checks
```

## License

MIT — see [LICENSE](LICENSE). Author: **Azra Bano**.

