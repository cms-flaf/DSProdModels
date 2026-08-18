# DSProdModels

Model definitions for [DSProd](https://github.com/cms-flaf/DSProd): production cards,
model-dependent plugins, gen fragments, setups, and any supporting tooling. It is mounted at
`models/` in DSProd.

This repository is **content, not a Python package** — there are no `__init__.py` files and
nothing here has to be importable by name. DSProd walks this tree and loads each `plugin.py`
straight from its path, which also leaves directory names free (e.g. `13p6TeV`, which is not a
valid Python identifier).

## Directory organization

Models are organized by **process → generator → center-of-mass energy**:

```
<process>/<generator>/<comEnergy>/
```

The center-of-mass energy is the **last** level on purpose: everything above it — the plugin and
the process/generator tooling — is then naturally shared across energies, and adding a new energy
for an existing model is just one more `<comEnergy>/` folder. Example:

```
X_HH/                                   process
├── README.md                          process documentation + links to the original sources
├── setups/                            production setups (one file per production, all eras)
├── filters/                           (optional) final-state filters, shared across generators/energies
└── MadGraph5_aMCatNLO/                generator
    ├── plugin.py                      the ProcessCustomization (registered), shared across energies
    ├── scripts/                       (optional) prodcard-generation scripts (e.g. parametrized in mX)
    ├── models/                        (optional) custom generator models, when not centrally available
    └── 13p6TeV/                       center-of-mass energy (LAST level)
        ├── cards/                     genproductions input cards for this energy
        └── fragments/                 CMSSW gen fragments — one per final state
```

**Name a process after what its cards actually produce**, not after a production mode or a final
state added later: `X_HH` produces an undecayed HH pair, while gluon fusion vs. VBF is a `cards/`
directory and the bbWW final states are `fragments/` inside it.

**Use the DAS tokens of the central samples** for those names, so a setup point reads like the
dataset it reproduces:

```
/GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800/...     the point `name`
 └──────┬──────┘            └──┬───┘
  production_mode            final_state          -> cards/<mode>/ , fragments/<final_state>.py
```

A new final state is then one more fragment (sharing the cards, the plugin and the gridpacks), and
a new production mode one more cards directory.

### What goes where

- **`<process>/`** — one physics process; its plugin registers under this `name`. Process-level
  material that is independent of generator and energy lives here: the process `README.md` (with
  links to the original request/recipe) and shared final-state `filters/`.
- **`<generator>/`** — the generator used (e.g. `MadGraph5_aMCatNLO`, `Powheg`); the name matches
  `genproductions_scripts/bin/<generator>` and `GridpackSpec.generator`. The **plugin** lives here,
  co-located with the tooling it needs: `scripts/` to (re)generate prodcards for different
  parameters (e.g. a mass scan) and `models/` for custom generator models not centrally available.
- **`<comEnergy>/`** — the innermost level (e.g. `13p6TeV`), holding only the energy-specific
  inputs: the genproductions `cards/` — one directory per production mode — and the gen
  `fragments/`, whose file names are the `final_state:` values a setup point can ask for. Both use
  the DAS tokens of the corresponding central samples.

Only `plugin.py`, `cards/`, one fragment, and the READMEs are required. `filters/`, `scripts/`,
and `models/` appear only when a model actually needs them.

## Discovery

DSProd (`dsprod/registry.py`) **walks this tree and loads every `plugin.py`** it finds, so a model
becomes available simply by adding its directory — there is no central registration list, and no
`__init__.py`, to edit. Each `plugin.py` must register a `ProcessCustomization` subclass with a
**unique `name`** via `@register_process`, and should resolve its cards/fragment relative to its own
location (via `os.path.dirname(__file__)` and `com_energy(era)`), so a model stays self-contained.

A plugin imports DSProd's framework classes (`dsprod.registry`, `dsprod.processes.base`), so the
plugins here only run inside a DSProd checkout, not as a standalone library.

## Adding a model

1. Create `<process>/<generator>/` with a `plugin.py` — a `ProcessCustomization` subclass
   decorated with `@register_process` and a unique `name`.
2. Add a `<process>/<generator>/<comEnergy>/` folder with the `cards/` and the `fragments/` for
   each energy you produce.
3. Document the process in `<process>/README.md`, with links to the original sources (McM request,
   genproductions recipe, gridpack, custom model, ...).
4. Add optional `filters/`, `scripts/`, `models/` where the process needs them.
5. Reference it from a DSProd [production setup](https://github.com/cms-flaf/DSProd) via
   `process: <name>` and advance the `models` submodule pointer in DSProd.
