"""X -> HH -> bb WW (resonant, narrow radion), MadGraph5_aMCatNLO.

Co-located per generator: this plugin is shared across center-of-mass energies. The
energy-specific inputs (genproductions cards, gen fragments) live in the `<comEnergy>/`
subdirectory next to this file; `com_energy(era)` selects which one. See the process README
(`../README.md`) for the physics and the links to the original sources.

Each point declares a decay `channel` — `SL` (single lepton, 2B2JLNu) or `DL` (double lepton,
2B2L2Nu) — which selects the gen fragment `<comEnergy>/fragments/<channel>.py`. The gridpack is
channel-independent (the Higgses leave MadGraph undecayed), so SL and DL of the same mass share
one gridpack.
"""

import os

from dsprod.registry import register_process
from dsprod.processes.base import GridpackSpec, Point, ProcessCustomization

_HERE = os.path.dirname(os.path.abspath(__file__))


@register_process
class XHHbbWW(ProcessCustomization):
    name = "X_HH_bbWW"
    generator = "MadGraph5_aMCatNLO"

    #: decay channels -> the central sample-name token for that final state
    CHANNELS = {"SL": "2B2JLNu", "DL": "2B2L2Nu"}

    #: process directory in the gridpacks store; the gridpack stops at the undecayed HH state,
    #: so it is shared with every other X->HH final state and is not stored under `name`
    gridpack_process = "X_HH"

    def com_energy(self, era=None):
        """Center-of-mass-energy subfolder for `era`. All current eras are Run3 (13.6 TeV);
        extend this mapping when the model spans several energies."""
        return "13p6TeV"

    def _cme_dir(self, era=None):
        return os.path.join(_HERE, self.com_energy(era))

    def _cards_dir(self, era=None):
        return os.path.join(self._cme_dir(era), "cards")

    def enumerate_points(self, process_cfg):
        events_per_job = process_cfg.get("events_per_job", 0)
        points = []
        for p in process_cfg["points"]:
            points.append(
                Point(
                    process=self.name,
                    name=p["name"],
                    params={
                        k: v for k, v in p.items() if k not in ("name", "events_total")
                    },
                    events_total=p["events_total"],
                    events_per_job=p.get("events_per_job", events_per_job),
                )
            )
        return points

    def gridpack(self, point, era=None):
        return GridpackSpec(
            generator=self.generator,
            cards_template=self._cards_dir(era),
        )

    def channel(self, point):
        """Decay channel of a point: `SL` (2B2JLNu) or `DL` (2B2L2Nu)."""
        ch = str(point.params.get("channel", "")).upper()
        if ch not in self.CHANNELS:
            raise ValueError(
                f"point {point.name!r}: `channel` must be one of "
                f"{sorted(self.CHANNELS)}, got {point.params.get('channel')!r}"
            )
        return ch

    def gen_fragment(self, point, era=None):
        return os.path.join(
            self._cme_dir(era), "fragments", f"{self.channel(point)}.py"
        )

    def gridpack_name(self, point):
        # channel-independent: the Higgses leave MadGraph undecayed, so SL and DL share a gridpack
        return f"Radion_hh_narrow_M{point.params['mass']}"

    def gridpack_rel_path(self, point, era=None):
        # mirror the DSProdModels layout in the DSProdGridpacks store
        return os.path.join(
            self.gridpack_process,
            self.generator,
            self.com_energy(era),
            self.gridpack_name(point),
            "gridpack.tar.xz",
        )

    def render_gridpack_cards(self, point, out_dir):
        cards = self._cards_dir()
        name = self.gridpack_name(point)
        mass = point.params["mass"]
        os.makedirs(out_dir, exist_ok=True)
        for card in ("proc_card", "run_card", "customizecards", "extramodels"):
            with open(os.path.join(cards, f"{card}.dat")) as f:
                text = f.read().replace("__NAME__", name).replace("__MASS__", str(mass))
            with open(os.path.join(out_dir, f"{name}_{card}.dat"), "w") as f:
                f.write(text)
        return name
