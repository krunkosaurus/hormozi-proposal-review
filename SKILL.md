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

### Agency brief enhancement
When the document is a marketing/design/creative agency brief, do more than critique positioning. Convert the review into a practical agency handoff that can drive execution.

Add or strengthen:
- the core offer hierarchy: market, dream outcome, proof, time to value, effort/sacrifice, pricing, risk reversal
- required proof assets before scaling paid ads, especially before/after examples, testimonials, screenshots, or specific proof captions
- campaign angles ranked by priority, not a scattered list of ideas
- exact ad copy banks: short headlines, longer headlines, primary text, CTAs, retargeting copy
- creative format briefs: static ads, UGC video, carousel, landing-page sections, proof placements
- objection handling and claims guidance so agencies avoid overpromising
- clear agency deliverables requested, including copy variants, creative concepts, video scripts, landing-page modules, and testing plans
- measurement notes focused on conversion metrics, not vanity metrics; prefer cost per paid customer, funnel conversion, and preview-to-purchase style metrics when relevant
- explicit “do/don’t” guardrails that prevent agencies from drifting into generic, pretty-but-useless creative

If the user asks for enhancement, write an improved markdown file rather than only summarizing feedback, and verify the file was written.

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

### Website / landing-page review
When reviewing a live website, do not stop at the homepage or hero section.

Follow the primary CTA path far enough to inspect the real conversion journey, including where possible:
- homepage or main landing page
- primary CTA destination
- pricing or membership details page
- application / enquiry / booking form
- FAQ or objections page

Specifically check for:
- whether pricing is shown, partially anchored, or hidden
- whether the next step matches buyer temperature
- whether the form asks for too much too early
- whether embedded third-party forms/iframes are hiding the real conversion flow; inspect `document.querySelectorAll('iframe')` and open form iframe URLs directly when the modal/page snapshot does not expose fields
- whether exclusivity language creates desire or just uncertainty
- whether proof is present near CTA moments, not just in brand copy
- whether objections are answered where the buyer actually hesitates

For premium or selective offers, distinguish between healthy exclusivity and needless ambiguity. Mystery can help positioning, but if proof and desire are not already strong, hidden pricing and vague qualification language usually create friction rather than prestige.

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

## Webpage Output Mode

Default behavior when this skill is used:

1. First deliver the normal human-readable review.
2. After the review, explicitly ask the user whether they want a local website version of the feedback.
3. Only generate the structured webpage payload and trigger the rendering flow if the user says yes.

The ask should be simple and direct, for example:
- `Do you want me to turn this into a local website version of the audit?`
- `Want this rendered as a local styled audit page too?`

If the user says yes, then produce the review in two layers:

1. the normal human-readable review
2. a structured payload matching `templates/review-webpage-data-template.json`

Use the structured payload so a renderer can generate a polished single-page audit website without inventing or re-parsing the review.

### Requirements for webpage mode

- Keep the content grounded in the actual review.
- Do not add sections the review did not support.
- Preserve the same blunt, practical tone.
- Keep field values concise enough to render well in cards, tables, and callout sections.
- Prefer arrays of bullets over giant paragraphs where possible.
- If a field is unknown, leave it empty or state `Unclear from provided materials`.
- Do not populate `meta.generated_for` with the chat user's name by default. Use `Internal Use Only`, leave it blank, or use an explicit client/company name only when requested.

### Preferred webpage payload sections

- `meta`
- `verdict`
- `dossier`
- `scorecard`
- `leaks`
- `strengths`
- `section_rewrites`
- `pricing`
- `action_plan`

### Renderer notes

- Use `scripts/render_offer_audit.py` to turn the structured payload into standalone HTML.
- Treat the cleaned static reference site at `/Users/krunkosaurus/Downloads/offer-audit-site-clean` as the base visual source of truth when refining the renderer, but cross-check final polish against the original reference site `https://offer-audit-jxwt37js.manus.space/` when the user asks for closer fidelity. Match the warm editorial audit style rather than inventing a generic dashboard: cream background, centered 896px report column, compact sticky mono nav, serif display headings, dark espresso verdict panel, thin ruled sections, flat bordered grids, orange score accents, and restrained teal callouts.
- Font sizing should not be too tiny: default body copy around 18px with generous line-height works closer to the original reference than the earlier 17px/dense version. If the user asks to bump size “by two clicks,” use body copy around 20px and widen the report shell at the same time (roughly 1024px page width / 960px inner content) so the page feels intentionally scaled rather than crowded. If they ask for one more overall notch larger after that, use body copy around 21px and widen the report shell again (roughly 1088px page width), then verify section grids still fit without horizontal overflow.
- When widening the report shell, re-check text measure section-by-section. Do not let full-width cards create long exhausting lines. For leak cards in particular, keep the card full-width but cap the internal text measure around 780px, use about 18px body text with ~1.55–1.6 line-height, warmer/darker body color, calmer mono tracking, and orange arrow bullets for fixes. This preserves the larger page while keeping `04 — Biggest Leaks` readable like the original reference.
- For the scorecard, prefer the original/clean site's compact `Area / Score / Notes` table pattern, with status shown under the score badge, unless the user explicitly requests a separate status column. Use a thin overall progress bar, orange uppercase interpretation line, dark espresso table header, pale row fills, square outlined score badges with state-colored text/borders rather than filled circular pills, and a thin line bar inside each row's score cell so the reader can see section progress at a glance. Webpage payloads should include `max_score_per_row` on the scorecard or `score_max` on each row; default to 0–2 only when not provided. On the larger layout, slightly enlarge score badges/status text so they remain legible.
- Keep dossier content in a flat two-column bordered grid and render `WHAT IS UNCLEAR` as a separate orange left-border callout, not as another dossier cell.
- Render `Five Critical Revenue Leaks` as pale peach/orange full-width cards with an orange left border and a single-column stack of `EVIDENCE`, `WHY IT HURTS`, `PRINCIPLE VIOLATED`, and `FIX`. Do not use a two-column leak grid; the original reference uses vertical editorial callout cards.
- Render `06 — Section Critique & Rewrites` with the heading `What to Say Instead` and comparison cards: `CURRENT`/`CURRENT (IMPLIED)` on cream/orange treatment and `BETTER` on pale teal/teal treatment. Avoid generic `Before`/`After` labels unless the user explicitly wants them. Match the original reference's quote-heavy rewrite style: wrap current and better copy in curly quotes, use italic quote treatment for the copy samples, keep current copy muted, and make better/strongest cards feel like direct replacement language rather than commentary. Support an optional third `STRONGEST` teal-emphasis card when payload data includes a stronger variant.
- For closer fidelity to the cleaned/reference site, mirror these section treatments too: strengths as individual pale green rows with green left borders (not a plain ruled bullet box); pricing as separate bordered cards with gaps and teal mono labels (not a shared table grid); action plan as three separate gap-separated cards with orange/teal/neutral left-border treatments. Inside action plan cards, render list items as clean right-arrow rows, not default bullets: orange arrows for `FIX THIS FIRST`, teal arrows for `THEN TEST THIS`, and muted/tan arrows for `DO NOT CHANGE YET`. Use grid/flex alignment so wrapped action items align under the text rather than under the arrow. Render funnel flow as teal step chips with arrow separators rather than a bullet list.
- Include the final `Blunt Recommendation` closing block after the funnel flow in the action section. Match the source style: full-width dark espresso card, small mono label, large serif recommendation headline, and muted cream supporting body text. If the payload lacks a dedicated `action_plan.blunt_recommendation`, derive the headline from the verdict quote/headline and the body from the verdict summary rather than omitting the block.
- Keep the nav/reference shell close to the source: opaque warm cream sticky nav, compact mono nav links, and a strong dark espresso bottom rule when matching the cleaned localhost/reference page.
- Match the reference site's generous horizontal divider rhythm around section headings: section number labels should not add extra bottom margin; `.rule-divider` should be visually substantial, about 2px high with roughly 40px vertical margin above and below. Avoid cramped `0 0 24px` divider spacing because it makes sections feel compressed versus the original Manus/reference audit page.
- After renderer changes, regenerate a known payload, render once through the workspace renderer and once through the installed skill renderer, compare with `cmp -s`, then visually inspect the key sections in the browser.
- Avoid third-party hosted page-builder/runtime scripts in final output; keep the rendered page self-contained.

### Webpage mode prompt pattern

Default interaction pattern:

- Use the skill to deliver the review first.
- Then ask whether the user wants a local website version of that audit.
- Only if they say yes, output the structured webpage payload matching `templates/review-webpage-data-template.json` and proceed with local rendering.

Example follow-up line:

`If you want, I can also turn this into a local styled audit webpage.`

If the user explicitly asks for the webpage immediately, you can skip the follow-up question and go straight into webpage mode.

Direct webpage-mode prompt pattern:

"Review this proposal using the Hormozi proposal review skill, then also output a structured webpage payload matching `templates/review-webpage-data-template.json` so the result can be rendered into a polished audit page."

## Deliverable Standard

A successful review should make it obvious:
- what the proposal is really selling
- why it will or will not convert
- what the top leverage fixes are
- what should be rewritten first
- what should not be scaled yet
