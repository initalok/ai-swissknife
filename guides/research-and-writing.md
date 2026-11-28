---
title: "Research & Writing"
section: guides
summary: "Cited literature synthesis combining OpenAlex academic graphs, Exa 3.0 neural search, Firecrawl Markdown extraction, and open research harnesses."
order: 5
---

[Home](../README.md) / Guides / Research & Writing

<!-- swissknife:begin status-banner -->
*Last verified: 2026-11-28 · All tracked links healthy ([System Status](../STATUS.md)) · [For AI Agents (`llms.txt`)](../llms.txt)*
<!-- swissknife:end -->

# Research & Writing

Reliable AI-assisted research separates **source gathering** (verifiable DOIs, primary docs, and clean Markdown extraction) from **synthesis and human verification**.

## Verified Research & Grounding Stack

<!-- swissknife:begin table tag=research -->
| Entry | Best Used For | Key Specs | Evidence | Primary Limitation |
| :--- | :--- | :--- | :--- | :--- |
| [Firecrawl](https://www.firecrawl.dev/) | Turning modern dynamic documentation sites into clean Markdown for research and RAG. | Keyless onboarding skill + 500 starter credits | Primary evaluation | Keyless usage is strictly IP-rate-limited; create a free API key for multi-page crawls. |
| [Jina Reader (r.jina.ai / s.jina.ai)](https://jina.ai/reader/) | One-line URL reading inside shell scripts and lightweight agents. | Keyless prefix + 10M free tokens with free API key | Official documentation | Unauthenticated prefix requests throttle quickly under automated batch loops. |
| [Exa 3.0 Neural Search](https://exa.ai/) | High-precision web discovery for research agents and technical literature scouting. | No card: $10/mo recurring credits (~2,500 Lite searches) | Official documentation | Deep search modes exhaust monthly free credits much faster than Lite searches. |
| [OpenAlex Academic Graph](https://docs.openalex.org/) | Primary literature review, DOI verification, and academic citation mapping. | Keyless: 100,000 requests/day forever | Official documentation | Pass ?mailto=you@domain.com in queries to enter the fast polite pool. |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Generating structured, cited background reports over mixed web and local documents. | Apache-2.0 | Official documentation | Audit every cited claim, date, and quantitative metric against primary sources before publishing. |
<!-- swissknife:end -->

## Step-by-Step Workflow

1. **Start with primary graphs, not raw web noise:** Pull peer-reviewed papers, DOIs, and citation graphs via **OpenAlex** (100,000 keyless requests/day; pass `?mailto=you@domain.com` for the polite pool).
2. **Extract live technical documentation cleanly:** Use **Exa 3.0** ($10/mo renewing free credits) for semantic discovery and **Firecrawl** or **Jina Reader** (`r.jina.ai/<url>`) for low-token Markdown extraction.
3. **Synthesize over mixed web + local sources:** Run **GPT Researcher** across gathered pages and local PDF/CSV folders, filing curated takeaways into your [Plain-Markdown Knowledge Vault](memory-and-knowledge.md).
4. **Audit every primary source manually:** Never publish quantitative claims, benchmarks, or dates without checking the primary URL or DOI yourself.

---

**Continue reading:** [Zero-Card Cloud](../worlds/cloud.md) · [Persistent Memory & Knowledge Loops](memory-and-knowledge.md)
