# Hormozi Proposal Review

A reusable Hermes skill for reviewing business proposals, landing pages, decks, pricing pages, screenshots, and mixed asset folders using a blunt, practical, Hormozi-inspired framework.

This skill is designed to:
- diagnose market, offer, proof, delivery, lead flow, and sales execution
- surface the biggest conversion leaks
- provide concrete rewrites instead of vague feedback
- stay grounded in a documented playbook and rubric

## Contents

- `SKILL.md` — the main Hermes skill definition
- `references/hormozi-playbook.md` — playbook grounding the review logic
- `references/hormozi-rubric.md` — scoring and diagnostic rubric
- `templates/review-output-template.md` — standard review output structure

## What it reviews

- single text documents
- screenshots and visual sales assets
- landing pages
- pricing pages
- sales decks
- folders of mixed proposal materials

## Output shape

The default review format includes:
1. Executive verdict
2. Proposal dossier
3. Scorecard
4. Biggest leaks
5. What is strong
6. Section-by-section critique
7. Rewrites
8. Considerations
9. Highest-leverage next actions

## Installation

To install into Hermes manually:

1. Clone this repository.
2. Copy the repository contents into your Hermes skills directory, typically:
   `~/.hermes/skills/business/hormozi-proposal-review`
3. Load the skill by name in Hermes: `hormozi-proposal-review`

## Invocation pattern

Use a prompt like:

`Review this proposal using the Hormozi proposal review skill. Be blunt, practical, and evidence-based. Apply the included playbook and rubric. Do not roleplay as Alex Hormozi. Diagnose market, offer, proof, delivery, lead flow, and sales execution in that order. Give concrete rewrites and a considerations section.`

## Notes

This is inspired by Hormozi-style offer logic, not an impersonation. The emphasis is operator-grade critique, evidence, and practical improvements.

## License

MIT
