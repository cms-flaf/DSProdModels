"""X -> HH (resonant, narrow radion), MadGraph5_aMCatNLO.

The cards produce `gg -> X -> HH` with both Higgs bosons **undecayed**, so this model is not tied
to a final state: a point picks one by naming a `channel`, which is simply the gen fragment
`<comEnergy>/fragments/<channel>.py` that decays the HH pair. Adding a final state therefore means
adding a fragment — nothing here changes. One gridpack serves them all, so the points of one mass
are produced from a single gridpack.

Co-located per generator: this plugin is shared across center-of-mass energies. The
energy-specific inputs (genproductions cards, gen fragments) live in the `<comEnergy>/`
subdirectory next to this file; `com_energy(era)` selects which one. See the process README
(`../README.md`) for the physics and the links to the original sources.
"""

import glob
import os

from dsprod.registry import register_process
from dsprod.processes.base import (
    GridpackSpec,
    Point,
    ProcessCustomization,
    events_per_era,
)

_HERE = os.path.dirname(os.path.abspath(__file__))


@register_process
class XHH(ProcessCustomization):
    name = "X_HH"
    generator = "MadGraph5_aMCatNLO"

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
        eras = process_cfg["eras"]
        points = []
        for p in process_cfg["points"]:
            points.append(
                Point(
                    process=self.name,
                    name=p["name"],
                    params={
                        k: v for k, v in p.items() if k not in ("name", "events_total")
                    },
                    # per era, so one setup covers every era it produces
                    events_total=events_per_era(p["events_total"], eras),
                    events_per_job=p.get("events_per_job", events_per_job),
                )
            )
        return points

    def gridpack(self, point, era=None):
        return GridpackSpec(
            generator=self.generator,
            cards_template=self._cards_dir(era),
        )

    def channels(self, era=None):
        """Final states available at this energy — one gen fragment each."""
        pattern = os.path.join(self._cme_dir(era), "fragments", "*.py")
        return sorted(
            os.path.splitext(os.path.basename(f))[0] for f in glob.glob(pattern)
        )

    def channel(self, point):
        """Final state of a point: the gen fragment that decays the HH pair."""
        ch = str(point.params.get("channel", ""))
        available = self.channels()
        if ch not in available:
            raise ValueError(
                f"point {point.name!r}: `channel` must be one of {available} "
                f"(a fragment in <comEnergy>/fragments/), got {point.params.get('channel')!r}"
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
            self.name,
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
