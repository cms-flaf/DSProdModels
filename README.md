# DSProdModels

Model definitions for [DSProd](https://github.com/cms-flaf/DSProd): the **production cards** and
the **model-dependent plugins**. It is mounted as the `dsprod_models` submodule of DSProd and
imported as the Python package `dsprod_models`.

## Layout

```
dsprod_models/                 (this repo, mounted at DSProd/dsprod_models)
├── __init__.py                imports every model subpackage (registration entry point)
└── <model>/
    ├── __init__.py            imports plugin.py
    ├── plugin.py              a ProcessCustomization subclass, @register_process
    ├── fragment.py            CMSSW gen fragment template
    └── cards/                 genproductions input cards (proc_card / run_card / …)
```

The reference model is `x_hh_bbww` (X→HH→bbWW resonant).

## How it plugs into DSProd

A DSProd [production setup](https://github.com/cms-flaf/DSProd) selects a model by its
`process:` key (the plugin's `name`). DSProd's registry imports `dsprod_models` to discover all
registered plugins. Each plugin resolves its cards/fragment relative to its own location, so a
model is self-contained here.

A plugin depends on DSProd's framework classes (`dsprod.registry`, `dsprod.processes.base`), so
this package is only usable inside a DSProd checkout — not as a standalone library.

## Adding a model

1. Add a subpackage `<model>/` with `plugin.py` (a `ProcessCustomization` subclass decorated with
   `@register_process`), a `fragment.py`, and a `cards/` directory.
2. Import it from the top-level `__init__.py`.
3. Reference it from a DSProd production setup via `process: <name>`.
