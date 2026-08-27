# DSProdModels — instructions for Copilot code review

The physics inputs for custom CMS Monte-Carlo production driven by
[DSProd](https://github.com/cms-flaf/DSProd): generator cards, gen fragments, per-process plugins
and the production setups that say what to produce, for which eras, and how many events.

**Read `FLAF/.github/copilot-instructions.md` first** for the shared rules on what a useful review
comment looks like and what not to flag, and `DSProd/.github/copilot-instructions.md` for the
production machinery this repository feeds.

## Why review matters more here than anywhere else

**This repository has no CI.** No formatting check, no consistency check, no integration test.
Review is the only gate between a change and a production that runs for days on the grid.

Nothing here executes at review time, so nothing fails fast. A wrong number in a setup or a wrong
parameter in a card produces samples that are valid files, pass every downstream task, and are
simply not the physics that was asked for. The cost of finding that out later is the whole
production.

Read a diff here the way you would read a configuration change to a running system: assume it
will be applied exactly as written, and ask what it will produce.

## Invariants

### Numbers must be derivable

Production setups (`*/setups/*.yaml`) carry `events_total` per era, and the existing files explain
in comments **how those numbers were derived** — a luminosity scaling from the central production,
then a unification rule across mass points, with the arithmetic written out.

A diff that changes an event count, adds an era, or adds a mass point must keep that derivation
truthful. Check the arithmetic against the stated rule, and flag a number that no longer follows
from the comment above it, or a comment left describing the previous numbers. A count changed
without its justification is the single most expensive kind of error this repository can contain:
too low and the sample is unusable, too high and the grid time is wasted.

### A card change invalidates what already exists

`cards/` (`run_card.dat`, `proc_card.dat`, `customizecards.dat`, `extramodels.dat`) and
`fragments/` determine the generated physics. Editing them changes what a **new** gridpack
produces while any gridpack already built from the old cards stays as it was. Ask whether the
change is meant to apply retroactively, and if so, whether the affected gridpacks and samples are
being regenerated. Silent divergence between a card and the samples produced from it is not
detectable downstream.

### Names are an interface

Points name a production mode and a final state using the **tokens the corresponding central
dataset uses on DAS**, and the plugin maps those onto a cards directory and a fragment. A renamed
token, a new production mode without its `PRODUCTION_MODES` entry, or a final state without a
matching fragment breaks the mapping — and it breaks it at production time, not at review time.

### Era coverage must be complete and intentional

`eras`, `nano_versions` and any per-era mapping must agree with each other and with the conditions
DSProd declares for those eras. An era listed in one and missing from another is a gap that only
appears when someone produces it. Note that Summer24 MC is shared across 2024, 2025 and 2026 — a
count given for 2024 covers all three.

### The gridpack store is not here

Gridpacks live in `cms-flaf/DSProdGridpacks` and are checked out sparsely with Git-LFS downloads
disabled. Never suggest committing a gridpack, a tarball or any other large binary to this
repository.

## Documentation must ship with the change

A PR must update the documentation **in the same PR** whenever it changes anything a user can
observe: a setup key, a point-naming convention, a supported production mode or final state, the
meaning of an existing field, or what a process requires.

Where it goes:

- the per-process `README.md` files (`<process>/README.md`, `<process>/<generator>/<...>/README.md`)
  carry the physics and the links to the original sources — keep them accurate;
- the plugin docstrings describe the naming contract and are read as documentation;
- anything about how DSProd *consumes* these files belongs in `DSProd/docs/`
  (`configuration/prod-setups.md`, `configuration/processes.md`), which is a **separate
  repository** and therefore a companion PR. Flag its absence.

The comments inside a setup file are documentation too: they are the only record of how its
numbers were obtained.

## Do not flag

- The generator card formats — `run_card.dat` and friends are MadGraph's, not ours to restyle.
- Verbose comment blocks in setups and plugins; here they are the derivation record, not clutter.
- Duplication between production modes or final states; they are kept explicit so each can be read
  on its own.
- Missing tests — nothing here is executable in isolation.

## Repository facts

Verified 2026-08-27; re-check before relying on any of it.

| | |
|---|---|
| Layout | `<process>/` (e.g. `X_HH/`) containing `README.md`, `setups/*.yaml`, and `<generator>/` (e.g. `MadGraph5_aMCatNLO/`) with `plugin.py` and `<comEnergy>/` holding `cards/<production_mode>/` and `fragments/<final_state>.py` |
| Consumed by | `cms-flaf/DSProd`, as the `models` submodule |
| Related | gridpacks in `cms-flaf/DSProdGridpacks` (CERN GitLab, sparse LFS); conditions in `DSProd/config/conditions_Run3.yaml` |
| CI | **none** — no workflows in this repository |
