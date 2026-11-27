[Home](../README.md) / Reference / Harnesses & Runtimes

*Last verified: 2026-11-27 · All tracked links healthy ([System Status](../STATUS.md))*

# Harnesses, Safety Proxies & Inference Runtimes

Practical reference for the control loops that execute agent workflows, the safety proxies that audit tool calls, and the engines that serve local weights.

## Agent Harnesses

### [Pi Coding Agent (+ @earendil-works/pi-durable)](https://github.com/earendil-works/pi) — *Building-Block Kernel*

Minimal, hackable agent loop (TUI, RPC, and SDK) featuring /tree DAG session branching, a built-in MCP + Codemode JavaScript sandbox, and first-party SQLite crash-resumable checkpoints.

- **When to use:** When you want full control over context assembly, clean compaction, and the highest-scoring official target for Hugging Face's RL harness adapters.
- **License:** `MIT` · **Evidence:** Primary evaluation
- **Limitation:** Intentionally omits built-in per-tool approval prompts; always pair with safeagents or an OS sandbox.

### [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) — *Plugin-Everything Platform*

Cordis-based agent platform where every subsystem—including the agent loop itself—is a hot-swappable plugin, paired with a read-only-by-default sandbox and sub-agent plugins.

- **When to use:** Building custom agent loops, interactive Creator Mode plugins, or multi-harness web sessions.
- **License:** `MIT` · **Evidence:** Official documentation
- **Limitation:** Fast-moving developer preview (0.2.3-alpha.2); pin plugin versions against breaking interface changes.

<details>
<summary>Show quickstart command</summary>

```bash
npx @deepseek-ai/dsh web
```

</details>

### [Hermes Agent (v0.23.4)](https://github.com/NousResearch/hermes-agent) — *Self-Improving Daemon*

Persistent autonomous agent featuring cross-session memory, autonomous skill authoring, cron scheduling, Telegram/ACP bridges, and official Hugging Face harness adapter support.

- **When to use:** Always-on background assistants, scheduled research digests, and multi-surface personal operations.
- **License:** `MIT` · **Evidence:** Official documentation
- **Limitation:** Does not auto-compact aggressively like Pi by default; cap thinking and context lengths on very large repositories.

### [OpenCode CLI](https://github.com/anomalyco/opencode) — *Terminal Coding CLI*

Vendor-agnostic terminal coding interface compatible with local OpenAI-compatible servers and backed by an official Hugging Face Qwen3.8-27B harness LoRA.

- **When to use:** Straightforward terminal software engineering with zero vendor lock-in.
- **License:** `MIT` · **Evidence:** Primary evaluation
- **Limitation:** Monitor context growth during multi-hour sessions; compaction is less aggressive than Pi.

## Safety Boundaries

### [Hugging Face safeagents Proxy](https://github.com/huggingface/safeagents)

Transparent OpenAI/Anthropic runtime proxy auditing every tool call via fast local scanning (atif-scan, ~10-20ms on Apple Silicon) and optional decision-model judges.

- **When to use:** Mandatory guard layer between autonomous coding harnesses (or unfiltered local models) and shell/filesystem tools.
- **Limitation:** Configure an explicit domain plugin rather than relying on empty defaults.

<details>
<summary>Show proxy command</summary>

```bash
safeagents start http://localhost:8000 --plugin hf://harness-hub/qwen-safeagents-plugin
```

</details>

## Inference & Media Runtimes

| Runtime | Best Used For | License | Key Limitation |
| :--- | :--- | :--- | :--- |
| [llama.cpp (Mainline GGUF Engine)](https://github.com/ggml-org/llama.cpp) | Primary local LLM server on NVIDIA workstations and cross-platform CLI deployments. | `MIT` | --no-mmap is deprecated (migrate to --load-mode none); pass -cuda graphs=0 if partial MoE offloading outputs gibberish. |
| [Unsloth Runtime & Studio](https://github.com/unslothai/unsloth) | Serving Dynamic v3.1 GGUFs, local Laya decision endpoints, or routing Anthropic-protocol clients to local models. | `Apache-2.0` | Keep Studio updated alongside mainline llama.cpp when adopting newly released quantization formats. |
| [Apple MLX (mlx-lm)](https://github.com/ml-explore/mlx-lm) | Primary local serving engine on Apple Silicon Macs (M-series Mac mini, MacBook Pro, Mac Studio). | `MIT` | Prompt prefill lags dedicated NVIDIA Tensor Cores; 32GB+ unified memory is recommended for comfortable 27B coding sessions. |
| [WanGP v20.12 (MMGP v4 + SageGP 1.0.2)](https://github.com/deepbeepmeep/WanGP) | Running Wan 2.2, LTX-2.5, and Qwen-Image-2.1 on 8GB-16GB consumer GPUs. | `Apache-2.0` | Install WGPKernels 1.5.0 and SageGP 1.0.2 (PyTorch 2.10; Triton 3.6+ required for RTX 50-series adaptive Sage2/3). |

---

**Continue reading:** [Harness Adapters Research](../research/harness-adapters.md) · [Local Models Reference](local-models.md)
