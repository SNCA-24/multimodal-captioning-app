# PORTFOLIO_CONTEXT

## Candidate profile
- Final semester MS in AI student
- Target hiring order: MLE first, DE second, DS third
- Applying for full-time roles
- Portfolio goal: appear engineering-first, reproducible, recruiter-friendly, and technically credible
- Main GitHub objective: show end-to-end ownership, architecture clarity, evaluation rigor, and practical relevance

## Portfolio positioning
This GitHub should communicate:
- Applied AI/ML engineer with strong data foundations
- Can build end-to-end ML systems, data pipelines, search/ranking workflows, and modern AI systems
- Stronger portfolio emphasis on MLE and DE than notebook-heavy DS work

## Repo polishing goal
This repository is being polished as a GitHub portfolio artifact, not as an academic submission.
The goal is to:
- remove academic / course-submission feel
- improve engineering clarity
- improve reproducibility
- surface the strongest technical signals quickly
- make the repo understandable to both recruiter skim and technical deep dive

## Repo-specific context
- Repo name: image-and-video-caption-generator
- One-line repo purpose: multimodal caption generation app for uploaded images and sampled video frames, with optional multilingual translation
- Why this repo matters for hiring: it shows an end-to-end inference application with frontend/backend boundaries, model integration, and user-facing AI workflow rather than only a notebook demo
- Current state: small academic demo with a clear app skeleton, but weakly documented, weakly reproducible, and thin on engineering proof; it currently reads more like a class project than a recruiter-facing MLE repo
- Target end state: a polished multimodal inference repo with a clean architecture story, reproducible setup, visible example outputs, lightweight evaluation, and enough engineering proof to support a credible MLE portfolio narrative
- Likely role relevance: strongest for MLE, weak for DE, moderate supporting value for DS

## Repo-specific strengths to preserve
- Preserve the frontend/backend split and the full product slice from upload -> API -> model inference -> rendered output
- Preserve the multimodal scope: image captioning, video frame captioning, and optional translation
- Preserve the small surface area and clear app boundary, since that makes the repo realistic to harden quickly
- Preserve any working BLIP / MarianMT integration already present in backend code

## Repo-specific weaknesses to fix
- Root README is too thin and does not explain setup, architecture, outputs, or limitations
- Frontend still contains academic framing and boilerplate that weakens hiring presentation
- Backend setup is not reproducible enough yet: missing dependency/env story and weak startup path
- Engineering proof is too weak: almost no meaningful tests, no CI, no deployment/run discipline, no clear technical judgment surfaced
- Evaluation is missing: no qualitative examples table, no latency discussion, no failure cases, and no tradeoff explanation

## Repo-specific polishing goal
This repo should be repositioned as:
- a small but polished multimodal inference system
- not a research-heavy ML repo
- not a coursework demo
- not a toy UI wrapper

The polished version should communicate:
- model-serving awareness
- API/UI integration
- practical multimodal inference design
- lightweight but real engineering discipline
- honest tradeoffs and limitations

## What Codex should optimize for in this repo
- Make the repo feel like a compact production-style inference app
- Emphasize architecture clarity, reproducibility, and demo quality over academic completeness
- Add just enough engineering proof to make the repo credible: setup, tests, CI, and stable run path
- Surface example outputs and failure cases so the repo has judgment, not just functionality
- Keep the improvements realistic and lightweight; do not over-engineer this repo beyond its natural scope

## Pin-worthiness expectation for this repo
- This repo is not a “pin now” candidate in its current state
- Best target outcome: polish first, then decide whether it becomes a long-term supporting pinned repo
- It should only be pinned if the final version clearly shows:
  - reproducible setup
  - strong README
  - visible example outputs
  - basic tests/CI
  - clean frontend/backend story
  - enough technical depth to avoid looking like a thin wrapper demo


## Final decision target
At the end of polishing, the repo should be classified as one of:
- Pin now
- Polish more, then pin
- Keep public but not pinned
- Low priority for further portfolio work