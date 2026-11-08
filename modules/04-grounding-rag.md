# Pillar 4: Search, Scraping, Reranking & Academic Grounding APIs
> Card-free, low-token-overhead grounding endpoints built for autonomous research and RAG agents.

| Role | Tool / Endpoint | Free Quota (No Card) | Technical Edge |
| :--- | :--- | :--- | :--- |
| **Keyless Web Search & Markdown Scraper** | [**Firecrawl (Keyless & Standard API)**](https://www.firecrawl.dev/) | Daily per-IP keyless quota + 500 free signup credits | Lowest token bloat in benchmarks (median 7,456 tokens/task vs 15K+ on raw HTML scrapers). |
| **Zero-SDK URL & PDF to Markdown** | [**Jina Reader (r.jina.ai / s.jina.ai)**](https://jina.ai/reader/) | Keyless URL prefix + 10,000,000 free tokens on API key creation | Prepend `https://r.jina.ai/` to any URL or PDF for instant LLM-clean Markdown without installing an SDK. |
| **Neural & Deep Agent Search** | [**Exa 3.0 (Lite, Answer, Deep Search)**](https://exa.ai/) | $10/month recurring free credits + $10 onboarding bonus (~2,500 Lite searches/mo @ 10 QPS) | Semantic neural search with controllable reasoning effort purpose-built for LLM tool calls. |
| **Pre-Chunked RAG Web Search** | [**Tavily Search API**](https://tavily.com/) | 1,000 API credits/month free forever (Researcher Plan) | Returns scored, pre-chunked factual context ready for direct prompt injection. |
| **Shared-Space Embeddings & Calibrated Reranking** | [**Cohere Embed 5 (Pro/Fast) & Rerank 5**](https://cohere.com/) | Free Trial Key: 10 Rerank calls/min, 20 Chat/min, 5 Image Embed/min (~1,000 calls/mo) | Index offline with Embed 5 Pro, query online with Embed 5 Fast (98.4% retention), and filter via Rerank 5 calibrated probability scores (32K context, native YAML/JSON). |
| **Academic & Citation Graph Grounding** | [**OpenAlex + Semantic Scholar + arXiv API**](https://openalex.org/) | 100,000 requests/day free (OpenAlex with polite email header) | 250M+ scholarly works, citation graphs, and open-access PDF links with zero paywalls. |
