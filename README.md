# Shopping Assistant (CrewAI) — Project Skeleton

A production-minded skeleton for a multi-agent shopping assistant using **CrewAI**.

## What you get
- CrewAI project structure (YAML-configured agents + tasks)
- Multi-agent pipeline: Planner → Researcher → Comparer → Final Advisor
- Basic guardrails to avoid age-restricted/unsafe categories
- Simple CLI entrypoint
- Clean separation: tools/ (I/O), services/ (logic), schemas/ (data)

## Quick start

### 1) Create & activate a virtual env
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
Using pip:
```bash
pip install -U pip
pip install -e .
```

### 3) Set environment variables
Copy the example file:
```bash
cp .env.example .env
```

If you want web search, set:
- `SERPER_API_KEY=...` (recommended with `SerperDevTool`)

Also set your model provider key(s) as needed (CrewAI supports many providers; see their LLM setup docs).

### 4) Run
```bash
python -m shop_assistant.main --query "best noise cancelling headphones under $200"
```

## Notes
- This is a **skeleton**: tools for specific retailers (Amazon/Walmart/BestBuy) are stubs you can fill in.
- Keep all “smart logic” in `services/` so prompts stay simple and testable.

## Project layout
See `src/shop_assistant/` for the crew, agents, tasks, schemas, and services.


### Google Shopping via Serper
This skeleton includes a custom CrewAI tool:

- **Google Shopping Candidates (Serper)** (`src/shop_assistant/tools/serper_shopping.py`)

It calls Serper’s Shopping endpoint and returns a normalized JSON list of candidates.
Set `SERPER_API_KEY` in your `.env` to enable it.
