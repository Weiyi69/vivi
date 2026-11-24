# Vivi Free Infrastructure Strategy

Status: planning

## Non-negotiable no-cost software baseline

Vivi will not require commercial AI APIs, paid hosting, paid storage, paid email, advertisements, or paid third-party services. Open-source infrastructure will be preferred.

## Planned zero-cost stack

- Next.js and FastAPI application code
- PostgreSQL and pgvector
- Ollama for local text generation
- Sentence Transformers or local ONNX models for embeddings
- Local filesystem storage
- Docker Compose for local and self-hosted operation
- Caddy as a free reverse proxy
- GitHub Actions for suitable free CI, subject to runner and usage limits

## Hardware assessment

Observed hardware is modest but suitable for small local models and development:

- CPU: Intel i5-10300H
- RAM: 16 GB
- GPU: RTX 2060 with 6 GB VRAM
- Storage: ample free disk capacity

The RTX 2060 is likely sufficient for quantized 1B-4B-class models or CPU fallback. Exact model selection requires Ollama installation and benchmark acceptance. Models above roughly 7B parameters are not a safe default for this machine.

## Candidate local generation

- Preferred initial benchmark: `Qwen3-4B-Instruct-2507`, because it is Apache-2.0 licensed and provides a useful small-model quality floor
- Hardware fallback: `Qwen2.5-1.5B-Instruct`, Apache-2.0 licensed
- Ollama package itself must be reviewed as it is added

Both model candidates require an Ollama artifact and license check before final selection. A 4B model is only a default candidate; the actual quantized weight size, Ollama memory footprint, 4K/8K-context performance, response quality, and instruction adherence must be benchmarked. A 1.5B model is the resource fallback. A 3B Qwen2.5 variant was not selected because the model family documentation identifies a non-Apache license for that variant.

## Candidate embeddings

- Preferred initial embedding model: `intfloat/multilingual-e5-base` (768 dimensions, MIT license)
- Upgrade candidate: `BAAI/bge-m3` (1024 dimensions, MIT license, greater memory and pipeline complexity)

The 768-dimensional E5 base model is the lower-risk MVP candidate because it is MIT licensed, broadly multilingual, and has a fixed modest embedding size. BGE-M3 supports more languages and more retrieval modes but is more resource-intensive and unnecessary for a first implementation. The selected model and exact revision must be recorded before embedding migrations are introduced.

## Operating cost reality

Students and the creator should not need software subscriptions, but electricity, internet, hardware, domains, TLS certificates, physical storage, and backup media can cost money. TLS certificates themselves can remain free with Caddy and ACME.
