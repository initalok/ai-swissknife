[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; **📘 Playbooks** &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)

# 📘 Core Playbooks (3 Deep Owned Runbooks)

> [!IMPORTANT]
> Core models, harnesses, backends, hot-swappable LoRAs, and mandatory guards below are **resolved implicitly** from the headless graph. Only flagship domain tools are declared per playbook.

## 📘 Coding, Web & Mobile Apps (`coding-and-apps`)

> **Verdict:** Pair your profile's best coding brain and harness (with auto-discovered HF LoRA adapters) against live Context7 docs, Playwright browser QA, and Sentry MobileBuildMCP.

### Implicitly Resolved Core Stack
- **Brains / Gateways:** `google-ai-studio` (🟢 `Fresh`), `zhipu-bigmodel` (🟢 `Fresh`), `nvidia-nim` (🟢 `Fresh`), `openrouter-free` (🟢 `Fresh`), `pollinations` (🟢 `Fresh`), `qwen3.8-27b` (🟢 `Fresh`), `qwen3-coder-next` (🟢 `Fresh`), `gemma-4` (🟢 `Fresh`), `inkling-2-mini` (🟢 `Fresh`)
- **Harnesses:** `pi` (🟢 `Fresh`), `deepseek-harness` (🟢 `Fresh`), `hermes-agent` (🟢 `Fresh`), `opencode` (🟢 `Fresh`)
- **Core Backends:** `llama-cpp` (🟢 `Fresh`), `unsloth-runtime` (🟢 `Fresh`), `mlx-lm` (🟢 `Fresh`)
- **Auto-Discovered Adapters (`adapts`):** `qwen38-super-adapter`
- **Attached Safety Layer (`guards`):** [**Laya 0.5 (Multimodal System-1 Decision Model)**](https://github.com/NandhaKishorM/laya), [**Hugging Face safeagents Runtime Proxy**](https://github.com/huggingface/safeagents)

### Verified Flagship Domain Tools

| Tool | Health | Canonical Repo |
| :--- | :--- | :--- |
| **Microsoft Playwright MCP** | 🟢 `Fresh` | `https://github.com/microsoft/playwright-mcp` |
| **Upstash Context7 (ctx7 + @upstash/context7-pi)** | 🟢 `Fresh` | `https://github.com/upstash/context7` |
| **Sentry MobileBuildMCP (Apple Builds/XCTest/LLDB)** | 🟢 `Fresh` | `https://github.com/getsentry/MobileBuildMCP` |
| **obra/superpowers (15 TDD & Spec Skills)** | 🟢 `Fresh` | `https://github.com/obra/superpowers` |

### Execution Workflow

1. Pin live framework doc lookups via Context7 (ctx7 or @upstash/context7-pi) inside repo AGENTS.md.
2. Use obra/superpowers to enforce Spec -> Red/Green TDD -> Verification before multi-file edits.
3. Verify web UI flows via Playwright MCP and Apple targets/simulators via Sentry MobileBuildMCP.

### Guardrails

- ⚠️ Pin local Context7 >= 2.1.3 (CVE-2026-75130); Playwright accessibility snapshots cannot pierce closed Shadow DOM.
- ⚠️ MobileBuildMCP covers Apple builds/simulators; pair with USB device tooling for physical Android/iPhone UI taps.

---

## 📘 Local Media Studio (Video, Image, Motion & Voice) (`local-media-studio`)

> **Verdict:** Anchor local 16GB video and RGBA image pipelines in WanGP v20.12 + Wan 2.2 / Qwen-Image-2.1, paired with Hyperframes for code-driven MP4s.

### Implicitly Resolved Core Stack
- **Brains / Gateways:** `google-ai-studio` (🟢 `Fresh`), `groq-cloud` (🟢 `Fresh`), `qwen-image-2.1` (🟢 `Fresh`), `wan-2.2` (🟢 `Fresh`)
- **Harnesses:** `pi` (🟢 `Fresh`), `deepseek-harness` (🟢 `Fresh`)
- **Core Backends:** `wangp` (🟢 `Fresh`)
- **Auto-Discovered Adapters (`adapts`):** None
- **Attached Safety Layer (`guards`):** None

### Verified Flagship Domain Tools

| Tool | Health | Canonical Repo |
| :--- | :--- | :--- |
| **HeyGen Hyperframes (HTML-to-MP4 Studio)** | 🟢 `Fresh` | `https://github.com/heygen-com/hyperframes` |
| **DaVinci Resolve MCP (Free & Studio Bridge)** | 🟢 `Fresh` | `https://github.com/hiteshK03/davinci-resolve-mcp` |
| **Gradium Phonon 31M WebGPU TTS (4.9ms)** | 🟢 `Fresh` | `https://github.com/blixt/phonon` |

### Execution Workflow

1. Use Hyperframes for crisp programmatic product demos, UI animations, and launch graphics.
2. Generate consistent AI video clips inside 5.9-15 GB VRAM via WanGP v20.12 (Extreme Chunker + MMGP v4).
3. Assemble final edits in DaVinci Resolve via MCP and synthesize fast English voiceovers via Phonon 31M.

### Guardrails

- ⚠️ Qwen-Image-2.1 is non-commercial (Qwen Research); swap to FLUX.2 Klein (Apache-2.0) for commercial graphics.

---

## 📘 Deep Research & Cited Literature Synthesis (`research-and-grounding`)

> **Verdict:** Combine GPT Researcher with card-free Exa 3.0, Firecrawl, Jina, and keyless OpenAlex (100K/day) for high-precision cited synthesis.

### Implicitly Resolved Core Stack
- **Brains / Gateways:** `google-ai-studio` (🟢 `Fresh`), `nvidia-nim` (🟢 `Fresh`), `openrouter-free` (🟢 `Fresh`), `qwen3.8-27b` (🟢 `Fresh`), `gemma-4` (🟢 `Fresh`)
- **Harnesses:** `pi` (🟢 `Fresh`), `hermes-agent` (🟢 `Fresh`)
- **Auto-Discovered Adapters (`adapts`):** None
- **Attached Safety Layer (`guards`):** None

### Verified Flagship Domain Tools

| Tool | Health | Canonical Repo |
| :--- | :--- | :--- |
| **GPT Researcher (gptr-mcp & Skill)** | 🟢 `Fresh` | `https://github.com/assafelovic/gpt-researcher` |
| **OpenAlex Polite Pool (100K/day Keyless)** | 🟢 `Fresh` | `https://openalex.org/` |
| **Exa 3.0 Neural Search ($10/mo Free)** | 🟢 `Fresh` | `https://exa.ai/` |
| **Firecrawl Keyless Scraper** | 🟢 `Fresh` | `https://www.firecrawl.dev/` |

### Execution Workflow

1. Pull open-access papers and citation graphs via OpenAlex (?mailto=...) and semantic discovery via Exa 3.0.
2. Run GPT Researcher across web sources and local PDF/CSV folders for cited draft reports.
3. Verify primary DOIs, dates, and exact numbers before treating any report as publication-ready.

### Guardrails

- ⚠️ Never cite autonomous research summaries without verifying primary source URLs.

---

[🏠 Hub](../README.md) &nbsp;·&nbsp; [☁️ Cloud](../book/cloud.md) &nbsp;·&nbsp; [🖥️ Local](../book/local.md) &nbsp;·&nbsp; [⚙️ Harnesses & RL](../book/harnesses-and-rl.md) &nbsp;·&nbsp; **📘 Playbooks** &nbsp;·&nbsp; [🧭 Spokes](../book/spokes.md) &nbsp;·&nbsp; [📡 Radar](../book/radar.md) &nbsp;·&nbsp; [🪦 Graveyard](../book/graveyard.md)
