# DSProdModels

Model definitions for [DSProd](https://github.com/cms-flaf/DSProd): production cards,
model-dependent plugins, gen fragments, and any supporting tooling. It is mounted as the
`dsprod_models` submodule of DSProd and imported as the Python package `dsprod_models`.

## Directory organization

Models are organized by **process → generator → center-of-mass energy**:

```
<process>/<generator>/<comEnergy>/
```

The center-of-mass energy is the **last** level on purpose: everything above it — the plugin and
the process/generator tooling — is then naturally shared across energies, and adding a new energy
for an existing model is just one more `<comEnergy>/` folder. Example:

```
X_HH_bbWW/                              process
├── README.md                          process documentation + links to the original sources
├── filters/                           (optional) final-state filters, shared across generators/energies
└── MadGraph5_aMCatNLO/                generator
    ├── plugin.py                      the ProcessCustomization (registered), shared across energies
    ├── scripts/                       (optional) prodcard-generation scripts (e.g. parametrized in mX)
    ├── models/                        (optional) custom generator models, when not centrally available
    └── 13p6TeV/                       center-of-mass energy (LAST level)
        ├── cards/                     genproductions input cards for this energy
        └── fragment.py                CMSSW gen fragment for this energy
```

### What goes where

- **`<process>/`** — one physics process; its plugin registers under this `name`. Process-level
  material that is independent of generator and energy lives here: the process `README.md` (with
  links to the original request/recipe) and shared final-state `filters/`.
- **`<generator>/`** — the generator used (e.g. `MadGraph5_aMCatNLO`, `Powheg`); the name matches
  `genproductions_scripts/bin/<generator>` and `GridpackSpec.generator`. The **plugin** lives here,
  co-located with the tooling it needs: `scripts/` to (re)generate prodcards for different
  parameters (e.g. a mass scan) and `models/` for custom generator models not centrally available.
- **`<comEnergy>/`** — the innermost level (e.g. `13p6TeV`), holding only the energy-specific
  inputs: the genproductions `cards/` and the gen `fragment.py`.

Only `plugin.py`, `cards/`, `fragment.py`, and the READMEs are required. `filters/`, `scripts/`,
and `models/` appear only when a model actually needs them.

## Discovery

`import dsprod_models` **walks this tree and loads every `plugin.py`** it finds, so a model becomes
available to DSProd simply by adding its directory — there is no central registration list to edit.
Each `plugin.py` must register a `ProcessCustomization` subclass with a **unique `name`** via
`@register_process`, and should resolve its cards/fragment relative to its own location (via
`os.path.dirname(__file__)` and `com_energy(era)`), so a model stays self-contained.

A plugin imports DSProd's framework classes (`dsprod.registry`, `dsprod.processes.base`), so this
package is only usable inside a DSProd checkout, not as a standalone library.

## Adding a model

1. Create `<process>/<generator>/` with a `plugin.py` — a `ProcessCustomization` subclass
   decorated with `@register_process` and a unique `name`.
2. Add a `<process>/<generator>/<comEnergy>/` folder with the `cards/` and `fragment.py` for each
   energy you produce.
3. Document the process in `<process>/README.md`, with links to the original sources (McM request,
   genproductions recipe, gridpack, custom model, ...).
4. Add optional `filters/`, `scripts/`, `models/` where the process needs them.
5. Reference it from a DSProd [production setup](https://github.com/cms-flaf/DSProd) via
   `process: <name>` and advance the `dsprod_models` submodule pointer in DSProd.
