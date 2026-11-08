# Pillar 2: Task-Routed Text & Coding Models (Benchmark-Filtered)
> Curated frontier generalists and niche specialists mapped to verified benchmarks and optimal free upstream gateways.

## Role: `agentic-terminal-coding`
*Multi-file edits, bash execution, autonomous debugging, and MCP tool loops.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **DeepSeek-V4-Pro / DeepSeek-V4-Flash** | `CN` / `MIT` | SWE-bench Verified: 80.6% (V4-Pro), 79.0% (V4-Flash) | `nvidia-nim`, `openrouter-free`, `unsloth-local` | Yes |
| **GLM-5.3-Flash / GLM-5.2** | `CN` / `MIT` | Terminal-Bench 2.1: 84.3% (5.3-Flash), 81.0% (5.2); Humanity's Last Exam: 55.3% | `zhipu-bigmodel`, `openrouter-free`, `unsloth-local` | Yes |
| **Kimi K3 / Kimi K2.6** | `CN` / `Open-Weights` | Terminal-Bench 2.1: 88.3% (K3); SWE-bench Verified: 80.2% (K2.6) | `nvidia-nim`, `openrouter-free` | Yes |

## Role: `scientific-deep-reasoning`
*PhD-level logic, math proofs, system architecture, and complex synthesis.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **Kimi K3** | `CN` / `Open-Weights` | GPQA Diamond: 93.5%; Humanity's Last Exam: 56.0% | `nvidia-nim`, `openrouter-free` | Yes |
| **MiniMax M3** | `CN` / `Open-API` | GPQA Diamond: 93.0% | `openrouter-free` | Yes |
| **Gemini 2.5 Pro / Gemini 3.8 Flash** | `US` / `Proprietary` | Top-tier multimodal reasoning + native code execution tool use | `google-ai-studio` | Yes |

## Role: `long-context-ingestion`
*Full codebase ingestion, multi-PDF synthesis, and 100K-1M+ token prompts.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.8 Flash / Gemini 2.5 Flash** | `US` / `Proprietary` | 1M context window backed by 1M TPM free quota (no 8K TPM wall) | `google-ai-studio` | Yes |
| **Llama 4 Scout** | `US` / `Open-Weights` | Up to 10M theoretical context; ultra-fast long-context recall on wafer-scale hardware | `cerebras-cloud`, `openrouter-free` | Yes |

## Role: `niche-fim-autocomplete`
*Sub-200ms IDE inline Fill-in-the-Middle (FIM) tab completion and fast diff refactoring.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **Codestral / Devstral 2** | `EU` / `Apache-2.0 / Proprietary` | 80+ languages FIM specialist with dedicated free endpoint | `mistral-plateforme` | Yes |
| **Qwen3-Coder-Next (80B MoE / 3B Active)** | `CN` / `Apache-2.0` | Activates only 3B params per token for near-instant repo-aware autocomplete | `openrouter-free`, `unsloth-local` | Yes |

## Role: `niche-fast-router-json`
*Sub-second intent classification, structured JSON extraction, and query rewriting.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen3.8-27B / Qwen3-32B** | `CN` / `Apache-2.0` | 2,000+ tok/s on Cerebras; rock-solid schema adherence | `cerebras-cloud`, `groq-cloud`, `unsloth-local` | Router/Edge Only |
| **Gemma 4 31B-it** | `US` / `Open-Weights` | High instruction-following density for lightweight routing pipelines | `google-ai-studio`, `openrouter-free`, `unsloth-local` | Router/Edge Only |
| **Mistral Small 4 (119B MoE)** | `EU` / `Apache-2.0` | Fast European multilingual & structured output workhorse | `mistral-plateforme` | Yes |

## Role: `niche-edge-and-gui-agents`
*On-device CPU/RAM execution and compact GUI/browser clicking automation.*

| Model | Origin / License | Benchmark Proof | Optimal Free Upstreams | Agent-Loop Ready |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen3-0.6B / Qwen3-4B (Unsloth UD-GGUF)** | `CN` / `Apache-2.0` | 30.6M+ monthly downloads; runs in minimal RAM for local pre-filtering | `unsloth-local` | Router/Edge Only |
| **UI-TARS / Runner H** | `CN / EU` / `Apache-2.0 / API` | Outperforms general frontier LLMs on OSWorld desktop/browser GUI grounding | `unsloth-local` | Yes |

