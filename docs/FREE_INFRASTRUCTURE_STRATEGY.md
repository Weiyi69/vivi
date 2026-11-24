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

- Preferred initial benchmark: Qwen2.5 3B or Qwen3 4B, if the selected model artifacts and license meet acceptance
- Ollama package itself must be reviewed as it is added
- Fallback: Qwen2.5 1.5B or 0.5B

The Ollama listing indicates Qwen2.5 models except 3B and 72B are Apache 2.0; the 3B variant was therefore not selected as the default. Qwen3 artifacts require final Hugging Face/Ollama license verification before adoption.

## Candidate embeddings

- `intfloat/multilingual-e5-base` (768 dimensions)
- `BAAI/bge-m3` (multilingual, 1024 dimensions, verify final model license)

Both candidates are locally hostable. The selected model must have a license suitable for the deployed use case and must be recorded in a final dependency/model decision.

## Operating cost reality

Students and the creator should not need software subscriptions, but electricity, internet, hardware, domains, TLS certificates, physical storage, and backup media can cost money. TLS certificates themselves can remain free with Caddy and ACME.
