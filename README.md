# Silicon-Agent Plan B: Local Sovereign Stack
## Autonomous 4G LTE Baseband Modem Design - RTX 4090 + Open-Weights Models

This repository implements the Plan B workflow from the Silicon-Agent Architecture specification.
Operates entirely within a single RTX 4090 (24 GB VRAM) and 64 GB system RAM using
open-weights models. No cloud API calls required - fully sovereign, air-gapped capable.

## Architecture

Same multi-agent topology as Plan A but with local models:

| Agent | Cloud (Plan A) | Local (Plan B) |
|---|---|---|
| Orchestrator | claude-sonnet-4 | Mistral-7B-Instruct (Q4_K_M) |
| 3GPP Librarian | claude-sonnet-4 + Pinecone | Nomic-embed-text + ChromaDB |
| RTL Engineer | claude-opus-4 | DeepSeek-Coder-33B (Q4_K_M) |
| Verification Eng | claude-opus-4 | DeepSeek-Coder-33B (Q4_K_M) |
| Judge | claude-sonnet-4 | Mistral-7B-Instruct (Q4_K_M) |
| PnR Lead | claude-sonnet-4 | CodeLlama-13B (Q4_K_M) |

## Memory Constraints

RTX 4090 24 GB VRAM allocation:

- 15 GB: Primary RTL Engineer (DeepSeek-Coder-33B Q4_K_M)
- 5 GB: Orchestrator/Judge (Mistral-7B Q4_K_M, shared)
- 3 GB: ChromaDB vector store + system overhead
- 1 GB: Buffer

Models swapped in sequence. No concurrent inference.

## Setup

```bash
pip install -r requirements.txt
# Download models
python scripts/download_models.py
# Ingest 3GPP specs
python scripts/ingest_specs.py --spec-dir ./specs/
# Run workflow
python main.py --target ofdm_modulator --spec 'TS 36.211 Section 6.3'
```

## Requirements

- NVIDIA RTX 4090 (24 GB VRAM minimum)
- 64 GB system RAM
- Ubuntu 22.04 LTS or newer
- CUDA 12.1+
- Python 3.11+
- Ollama (model serving)

## Directory Structure

```
agents/           Agent class definitions (local model variants)
workflows/        LangGraph pipeline (local orchestration)
tools/            ChromaDB search, artifact store, spec ingestion
scripts/          Model download, spec ingestion, utilities
specs/            Place 3GPP spec PDFs here (not tracked in git)
rtl/              Generated SystemVerilog artifacts
pnr/              OpenLane configuration
```

## Reference

Based on silicon_agent_architecture.md by jaketheclaw.
Full spec: https://github.com/jaketheclaw/markdown/blob/main/silicon_agent_architecture.md
