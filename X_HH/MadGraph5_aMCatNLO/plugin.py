"""X -> HH (resonant), MadGraph5_aMCatNLO.

The cards produce `X -> HH` with both Higgs bosons **undecayed**, so this model is tied to neither
a production mode nor a final state. A point names both, using the tokens the corresponding
central dataset uses on DAS
(`GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800` -> production mode `GluGlutoRadion`, final state
`2B2JLNu`):

    production_mode: GluGlutoRadion    -> cards      <comEnergy>/cards/GluGlutoRadion/
    final_state: 2B2JLNu               -> fragment   <comEnergy>/fragments/2B2JLNu.py

Both are open sets: another final state is another fragment, and another production mode (VBF, …)
is another cards directory plus one `PRODUCTION_MODES` entry — the tasks and the gridpack store
layout stay as they are. Final states of one production point share a gridpack, since the decays
happen after the generator.

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

#: How the hard process is produced. The key is the DAS production-mode token, which names both the
#: cards directory here and the production-mode level of the gridpack store; `gridpack` is the
#: gridpack naming, which must carry the production mode itself, because a production stores its
#: gridpacks flat (`<output>/gridpacks/<gridpack-name>/`).
PRODUCTION_MODES = {
    "GluGlutoRadion": {"gridpack": "GluGlutoRadiontoHH_M-{mass}"},
}

#: production mode of a point that does not name one (and of a setup with no default)
DEFAULT_PRODUCTION_MODE = "GluGlutoRadion"


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

    # ---- production mode ----------------------------------------------------
    def production_mode(self, point):
        """Production mode of a point, as the DAS token (e.g. `GluGlutoRadion`)."""
        mode = str(point.params.get("production_mode", DEFAULT_PRODUCTION_MODE))
        if mode not in PRODUCTION_MODES:
            raise ValueError(
                f"point {point.name!r}: unknown `production_mode` {mode!r}; "
                f"known modes are {sorted(PRODUCTION_MODES)}"
            )
        return mode

    def _cards_dir(self, point, era=None):
        return os.path.join(self._cme_dir(era), "cards", self.production_mode(point))

    # ---- final state --------------------------------------------------------
    def final_states(self, era=None):
        """Final states available at this energy — one gen fragment each, named after the DAS
        final-state token."""
        pattern = os.path.join(self._cme_dir(era), "fragments", "*.py")
        return sorted(
            os.path.splitext(os.path.basename(f))[0] for f in glob.glob(pattern)
        )

    def final_state(self, point):
        """Final state of a point: the gen fragment that decays the HH pair."""
        fs = str(point.params.get("final_state", ""))
        available = self.final_states()
        if fs not in available:
            raise ValueError(
                f"point {point.name!r}: `final_state` must be one of {available} "
                f"(a fragment in <comEnergy>/fragments/), got "
                f"{point.params.get('final_state')!r}"
            )
        return fs

    # ---- the ProcessCustomization interface ---------------------------------
    def enumerate_points(self, process_cfg):
        events_per_job = process_cfg.get("events_per_job", 0)
        default_mode = process_cfg.get("production_mode", DEFAULT_PRODUCTION_MODE)
        eras = process_cfg["eras"]
        points = []
        for p in process_cfg["points"]:
            params = {k: v for k, v in p.items() if k not in ("name", "events_total")}
            params.setdefault("production_mode", default_mode)
            points.append(
                Point(
                    process=self.name,
                    name=p["name"],
                    params=params,
                    # per era, so one setup covers every era it produces
                    events_total=events_per_era(p["events_total"], eras),
                    events_per_job=p.get("events_per_job", events_per_job),
                )
            )
        return points

    def gridpack(self, point, era=None):
        return GridpackSpec(
            generator=self.generator,
            cards_template=self._cards_dir(point, era),
        )

    def gen_fragment(self, point, era=None):
        return os.path.join(
            self._cme_dir(era), "fragments", f"{self.final_state(point)}.py"
        )

    def gridpack_name(self, point):
        # final-state independent: the Higgses leave MadGraph undecayed, so every final state of
        # one production point shares this gridpack
        template = PRODUCTION_MODES[self.production_mode(point)]["gridpack"]
        return template.format(**point.params)

    def gridpack_rel_path(self, point, era=None):
        # the DSProdGridpacks store mirrors this model's layout level for level:
        # <process>/<generator>/<comEnergy>/<production_mode>/<gridpack-name>/
        return os.path.join(
            self.name,
            self.generator,
            self.com_energy(era),
            self.production_mode(point),
            self.gridpack_name(point),
            "gridpack.tar.xz",
        )

    def render_gridpack_cards(self, point, out_dir):
        cards = self._cards_dir(point)
        name = self.gridpack_name(point)
        mass = point.params["mass"]
        os.makedirs(out_dir, exist_ok=True)
        for card in ("proc_card", "run_card", "customizecards", "extramodels"):
            with open(os.path.join(cards, f"{card}.dat")) as f:
                text = f.read().replace("__NAME__", name).replace("__MASS__", str(mass))
            with open(os.path.join(out_dir, f"{name}_{card}.dat"), "w") as f:
                f.write(text)
        return name
