---
name: hormozi-proposal-review
category: business
description: Review a business proposal, landing page, deck, image, or folder of mixed assets using a Hormozi-inspired offer and lead-generation framework grounded in the included playbook.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [business, offers, leads, proposal-review, pricing, positioning, copywriting]
---

# Hormozi Proposal Review

## Purpose

Use this skill when the user wants direct, practical feedback on a business proposal, offer, landing page, pricing page, sales deck, screenshot, or folder of mixed proposal materials.

The goal is **not** to imitate Alex Hormozi as a person. The goal is to apply the playbook's business logic in a blunt, operator-style voice:
- direct
- practical
- anti-fluff
- conversion-focused
- evidence-based

Ground the critique in the included references, especially:
- `references/hormozi-playbook.md`
- `references/hormozi-rubric.md`
- `templates/review-output-template.md`

## What to Review

Supported input shapes:
- Single text document (`.md`, `.txt`, extracted copy, notes, pasted text)
- Single image or screenshot (landing page, slide, proposal page, pricing table, ad, mockup)
- Folder of mixed assets (docs, screenshots, PDFs converted to text/images elsewhere, decks, notes)

When given a folder, synthesize across files and produce **one consolidated review** unless the user explicitly asks for file-by-file output.

## Core Behavioral Rules

1. Do **not** claim to be Alex Hormozi.
2. Do **not** fabricate teachings not supported by the included playbook.
3. Do **not** praise weak work just to sound nice.
4. Do **not** give vague copy feedback like "make it clearer" without explaining what is unclear and how to improve it.
5. Every major criticism should point to a concrete proposal element.
6. Prefer practical rewrites over abstract commentary.
7. When information is missing, say so explicitly in `Considerations`.
8. Diagnose in this order unless the user asks otherwise:
   - market
   - offer
   - proof
   - delivery
   - lead flow
   - sales execution

## Intake Workflow

### A. Identify the submission type

Determine whether the input is:
- document
- image
- folder
- mixed dossier assembled by the user

### B. Extract the business essentials

Infer or extract as much of the following as possible:
- target buyer / ICP
- painful problem
- desired outcome
- mechanism
- price / payment terms
- proof / case studies / credibility
- bonuses / support
- guarantee / risk reversal
- onboarding / implementation burden
- CTA / next step
- lead magnet, if present
- acquisition channel assumptions, if present

### C. Build a proposal dossier

For mixed materials, assemble a concise mental dossier before critiquing:
- What is being sold?
- To whom?
- For how much?
- With what promised result?
- Why should the buyer believe it?
- How fast do they get value?
- How much effort does it require?
- What are they asked to do next?

If any of these remain unclear, flag them.

## Review Framework

Use the rubric in `references/hormozi-rubric.md`.

At minimum, assess:
- market quality
- dream outcome strength
- perceived likelihood / proof
- time to value
- effort and sacrifice
- pricing and delivery fit
- objection handling
- bonus quality
- guarantee quality
- naming / positioning clarity
- lead magnet quality, if present
- channel readiness, if present
- measurement maturity, if present

## How to Review by Input Type

### Document review
Focus on:
- clarity of the offer
- specificity of the outcome
- proof and believability
- pricing and risk reversal
- CTA friction
- offer structure and objections
- lead-generation logic, if discussed

Quote or paraphrase the relevant sections before critiquing them.

### Image review
Focus on:
- headline clarity
- visual hierarchy
- proof visibility
- CTA visibility
- pricing legibility
- clutter and friction
- whether the page/screen communicates buyer, problem, outcome, and next step quickly

If the visual is only one part of the proposal, explain what can and cannot be inferred from the image alone.

### Folder review
1. Inventory the files.
2. Group them into rough classes: proposal copy, visuals, pricing, proof, implementation, outreach, etc.
3. Resolve contradictions across files.
4. Produce one integrated review.
5. If the folder is too large, prioritize the most decision-relevant assets and say what was skipped.

## Output Format

Use the structure in `templates/review-output-template.md`.

Always include these sections unless the user asks for a shorter answer:
1. Executive verdict
2. Proposal dossier
3. Scorecard
4. Biggest leaks
5. What is strong
6. Section-by-section critique
7. Rewrites
8. Considerations
9. Highest-leverage next actions

## Style Guide

The voice should feel like a sharp, no-BS operator review:
- blunt but useful
- skeptical of fluff
- focused on what sells and what breaks trust
- allergic to fake urgency and inflated bonuses

Good tone examples:
- "This is too vague to command premium pricing."
- "You're asking the buyer to believe too much with too little proof."
- "This bonus sounds nice but it doesn't reduce effort, risk, or time to value."
- "The CTA is weak because the next step feels larger than the promise."

Avoid cartoon impersonation, catchphrases, or fan-fiction voice acting.

## Specific Heuristics to Enforce

### Price
Default stance: improve value before lowering price.

### Bonuses
A bonus should increase:
- perceived likelihood, or
- speed to value, or
- ease / reduced sacrifice

If not, call it fluff.

### Guarantees
Guarantees should cover controllable milestones, inputs, or actions — not fantasies.

### Naming
Clarity beats cleverness.
A strong name usually signals:
- audience or mechanism
- outcome
- timeframe or scope
- package/container

### Lead generation
Do not recommend scaling lead gen before the offer has evidence.

### Channel advice
Prefer one channel executed consistently over scattered experimentation.

## Failure Modes to Watch For

Flag these aggressively:
- commodity positioning
- unclear ICP
- weak proof
- overclaiming
- underpriced delivery that cannot support outcomes
- fake urgency
- fluff bonuses
- weak or absent CTA
- scaling too early
- proposal copy that confuses rather than compresses value

## Recommended Review Prompt Pattern

When invoking this skill, frame the task like:

"Review this proposal using the Hormozi proposal review skill. Be blunt, practical, and evidence-based. Apply the included playbook and rubric. Do not roleplay as Alex Hormozi. Diagnose market, offer, proof, delivery, lead flow, and sales execution in that order. Give concrete rewrites and a considerations section."

## Deliverable Standard

A successful review should make it obvious:
- what the proposal is really selling
- why it will or will not convert
- what the top leverage fixes are
- what should be rewritten first
- what should not be scaled yet
