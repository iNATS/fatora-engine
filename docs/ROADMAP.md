# Roadmap

## Phase 0 — validate (week 1)
- [ ] Interview 15 target users: integrators, accountants and SMB operators.
- [ ] Document current workflow, volume, error costs and privacy constraints.
- [ ] Confirm document types and initial locale priorities.
- [ ] Verify project name and license compatibility.

**Exit gate:** 5 interviewees independently confirm a painful workflow; 3 agree to test an early build.

## Phase 1 — contract and baseline (week 2)
- [ ] Finalize invoice/receipt JSON schema.
- [ ] Implement adapter protocol.
- [ ] Add Decimal-based deterministic validation.
- [ ] Add synthetic Arabic/English mixed-script fixtures.
- [ ] Define benchmark metrics and data provenance.

**Exit gate:** schema and validation tests pass.

## Phase 2 — MVP extraction (weeks 3–4)
- [ ] Integrate first OCR/layout adapter.
- [ ] Implement PDF and image ingestion.
- [ ] Extract header fields and line items.
- [ ] Attach evidence and confidence where available.
- [ ] Add CLI and local REST endpoint.
- [ ] Dockerize and document privacy defaults.

## Phase 3 — evaluation (weeks 5–6)
- [ ] Add second engine adapter for comparison.
- [ ] Publish field-level metrics and error taxonomy.
- [ ] Add Python SDK examples and batch mode.
- [ ] Invite 5–10 design partners.

## Phase 4 — community release (weeks 7–8)
- [ ] Publish v0.1.0.
- [ ] Add contribution guide and good first issues.
- [ ] Add CI and dependency scanning.
- [ ] Publish dataset cards and license manifests.
- [ ] Run public feedback cycle.

## Longer term

TypeScript SDK, review UI, more locales, procurement/expense documents, plugin ecosystem and benchmark leaderboard.
