"""DSProd model definitions.

Each model is a subpackage holding its production cards, gen fragment, and a
``ProcessCustomization`` plugin that registers itself with DSProd via
``@register_process``. Importing this package imports every model subpackage, so a model
becomes available to DSProd simply by being listed here.

This package is consumed inside a DSProd checkout (it imports ``dsprod.*``); it is not a
standalone library. It is mounted as the ``dsprod_models`` submodule of DSProd.
"""

from . import x_hh_bbww  # noqa: F401
