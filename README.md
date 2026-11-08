# AI SWISS KNIFE // ONE-PAGE SPATIAL ARCHITECTURE
> **Minard Token-Pipe Routing • Barycentric Trade-Off Space • Top-Down Modality Matrix** — Built on Stone Librande's *One-Page Design Philosophy* and Katie Dill's *Opinionated Harness & Craft*.

![AI Swiss Knife One-Page Architectural Blueprint](poster.svg)

## ⚡ Opinionated CLI Harness (`./ask.py`)
Instead of hunting through fragmented wiki pages, query the routing engine directly from your terminal or agent harness:

```bash
python ask.py route coding-agent   # Get primary/fallback endpoints & .env for 20K-token coding loops
python ask.py route repo-1m        # Route 200K-1M context prompts without hitting 8K TPM walls
python ask.py route deep-reason    # Route PhD logic/math to Kimi K3 (93.5% GPQA) / Gemini 2.5 Pro
python ask.py route fast-json      # Route 2,000+ tok/s structured JSON extraction to Cerebras
python ask.py env coding-agent > .env.ai
python ask.py check                # Live HTTP latency & status check across all 9 gateways
python ask.py all                  # Sync upstream GitHub repos -> Lint graph -> Render poster.svg & index.html
```

## 🧭 Quick CLI Route Reference (Single-Glance Index)
| Intent (`./ask.py route <id>`) | Primary Model & Gateway | Verified Benchmark / Pipe Edge | Fallback Route | Blocked Trap |
| :--- | :--- | :--- | :--- | :--- |
| **`coding-agent`** (Agentic Coding & Terminal CLI) | `glm-5.3-flash` via [**Z.ai GLM**](https://open.bigmodel.cn/) | 84.3% Terminal-Bench 2.1 | 79.0% SWE-bench (DeepSeek-V4-Flash) | `gemini-3.8-flash` (Gemini API) | ✗ `Groq LPU` (8K TPM cap < 20K single agent turn) |
| **`deep-reason`** (Scientific & PhD Logic Synthesis) | `moonshotai/kimi-k3` via [**NVIDIA NIM**](https://build.nvidia.com/) | 93.5% GPQA Diamond | 56.0% Humanity's Last Exam | `gemini-2.5-pro` (Gemini API) | ✗ `Pollinations` (Shared community capacity drops long reasoning chains) |
| **`repo-1m`** (Full Repo / Multi-PDF Ingestion) | `gemini-3.8-flash` via [**Gemini API**](https://aistudio.google.com/) | 1M Effective Free Context + 1M TPM Pipe | `llama-4-scout` (Cerebras) | ✗ `Groq LPU` (Truncated by 8K TPM ceiling) |
| **`fim-ide`** (IDE Inline Autocomplete (FIM)) | `codestral-latest` via [**Mistral AI**](https://console.mistral.ai/) | 80+ Language FIM Specialist (1B tok/mo free tier) | `qwen3-coder-next-80b-a3b` (Unsloth Local) | ✗ `NVIDIA NIM` (Cold-start queue latency too high for keystroke FIM) |
| **`fast-json`** (Ultra-Fast Intent Router & JSON) | `qwen-3-32b` via [**Cerebras**](https://cloud.cerebras.ai/) | 2,000+ tok/s wafer-scale structured output | `qwen3.8-27b` (Groq LPU) | ✗ `Gemini API` (15 RPM limit bottlenecks high-QPS micro-routing) |
| **`voice-audio`** (Real-Time Voice (STT / TTS / Duplex)) | `whisper-large-v3` via [**Groq LPU**](https://console.groq.com/) | 20 RPM / 2,000 RPD free STT + Fish S2.1 Pro / Voxtral TTS | `voxtral-tts` (Mistral AI) | ✗ `Cerebras` (Text-only inference hardware) |
| **`rag-grounding`** (Web Grounding, Scrape & Rerank) | `firecrawl-keyless + cohere-rerank-5` via [**Gemini API**](https://aistudio.google.com/) | 7,456 median tok/scrape (Firecrawl) + Embed 5 Pro/Fast shared space | `mistral-ocr-4` (Mistral AI) | ✗ `Groq LPU` (No native search/rerank endpoint) |

---
*Interactive War Room Canvas: open `index.html` locally or enable GitHub Pages on this repository.*
