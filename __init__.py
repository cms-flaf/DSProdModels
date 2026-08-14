"""DSProd model definitions.

Models are organized as ``<process>/<generator>/<comEnergy>/`` (see README.md), with the
center-of-mass energy as the *last* level so that the plugin and the process/generator tooling
above it are shared across energies. Each generator directory holds a ``plugin.py`` that
registers a ``ProcessCustomization`` via ``@register_process``.

Importing this package walks the tree and loads every ``plugin.py``, so a model becomes
available simply by adding its directory — there is no central registration list to edit.

This package is consumed inside a DSProd checkout (plugins import ``dsprod.*``); it is not a
standalone library. It is mounted as the ``dsprod_models`` submodule of DSProd.
"""

import importlib.util
import pathlib
import re
import sys

_ROOT = pathlib.Path(__file__).resolve().parent


def _load_plugins():
    for plugin_path in sorted(_ROOT.rglob("plugin.py")):
        rel = plugin_path.relative_to(_ROOT).with_suffix("")
        # synthesize a unique, valid module name from the path (dir names may start with a
        # digit, e.g. 13p6TeV, so sanitize rather than use the path parts verbatim)
        suffix = "_".join(re.sub(r"\W", "_", part) for part in rel.parts)
        mod_name = f"dsprod_models._plugins.{suffix}"
        spec = importlib.util.spec_from_file_location(mod_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)


_load_plugins()
