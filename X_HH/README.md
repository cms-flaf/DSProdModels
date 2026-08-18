# X → HH (resonant)

Resonant di-Higgs signal: a narrow spin-0 resonance (radion) produced by gluon fusion and decaying
to a pair of Higgs bosons, `gg → X → HH`. Points are a resonance-mass scan; the mass lives in the
gridpack.

**The cards stop at the undecayed HH pair**, which is why the model is called `X_HH` and not after
a final state. The decays are done by the CMSSW gen fragment, which a point selects by name:

```yaml
channel: SL      # -> MadGraph5_aMCatNLO/<comEnergy>/fragments/SL.py
```

Adding a final state is therefore just adding a fragment — the plugin, the cards and the gridpacks
are untouched, and the new final state shares the gridpacks with the existing ones.

- **Registered name:** `X_HH` (the `process:` key in a DSProd production setup).
- **Generator:** `MadGraph5_aMCatNLO` (LO gridpack) + Pythia8 (CP5) hadronization.
- **Final states shipped:** `SL` — bbWW single lepton (`2B2JLNu`); `DL` — bbWW double lepton
  (`2B2L2Nu`).

## Layout

```
setups/                  production setups (one file covers every era)
MadGraph5_aMCatNLO/
├── plugin.py            the ProcessCustomization for this process/generator
└── 13p6TeV/
    ├── cards/           genproductions cards (see cards/README.md for the recipe)
    └── fragments/       one per final state; the file name IS the `channel:` value
        ├── SL.py        bbWW single lepton (2B2JLNu)
        └── DL.py        bbWW double lepton (2B2L2Nu)
```

## Production setup

`setups/Run3_XHHbbWW.yaml` — 44 samples (22 masses × SL/DL) for every era central production
misses. **One file for all of them**: `events_total` is given per era, so there is no per-era copy
to keep in sync.

```yaml
  - name: GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800
    mass: 800
    spin: 0
    channel: SL
    events_total:
      Run3_2023: 207000
      Run3_2023BPix: 112000
      Run3_2024: 2845000
```

| Era | Covers | Events |
|---|---|---|
| Run3_2023 | 2023 | 6.3 M |
| Run3_2023BPix | 2023BPix | 3.4 M |
| Run3_2024 | 2024 + 2025 + 2026 | 86.3 M |

An era a point does not list simply produces nothing for it. Subsets and short checks are
command-line options of the DSProd tasks (`--points '<glob>'`, `--test <n-events>`), not separate
setups.

**Event targets** reproduce the central per-mass statistics scaled by integrated luminosity:

```
N(mass, channel, era) = [ N_2022 + N_2022EE ] / 34664 pb⁻¹ × L(era) ,  rounded to 1k
```

with `L` = 17964 pb⁻¹ (2023), 9677 pb⁻¹ (2023BPix) and 246522 pb⁻¹ (2024+2025+2026, which share the
Summer24 MC). This preserves the central production's own mass dependence — it used ~11.5 events/pb⁻¹
up to ~2 TeV and ~2.9 events/pb⁻¹ above, so high masses stay proportionally smaller.

## Original sources

- **genproductions recipe** — MadGraph cards follow
  [`cms-sw/genproductions` · `bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0`](https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant),
  template `Radion_hh_narrow_M900`. Details and the per-card breakdown are in
  [`MadGraph5_aMCatNLO/13p6TeV/cards/README.md`](MadGraph5_aMCatNLO/13p6TeV/cards/README.md).
- **Custom model** — `heft_radion`, packaged centrally as `dibosonResonanceModel.tar.gz` and
  fetched by `gridpack_generation.sh` from `cms-project-generators` (referenced in
  `extramodels.dat`); nothing is shipped from this repo.
- **Gen fragments** — taken verbatim from the McM requests of the corresponding central samples:
  [`B2G-Run3Summer22EEwmLHEGS-00612`](https://cms-pdmv.cern.ch/mcm/requests?prepid=B2G-Run3Summer22EEwmLHEGS-00612)
  (SL, `2B2JLNu`) and
  [`B2G-Run3Summer22EEwmLHEGS-00656`](https://cms-pdmv.cern.ch/mcm/requests?prepid=B2G-Run3Summer22EEwmLHEGS-00656)
  (DL, `2B2L2Nu`).
- **Central gridpacks** — the standard mass points exist on cvmfs under
  `/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/.../GF_HH_Spin0/Radion_hh_narrow_M<mass>_*`
  and are mirrored into [DSProdGridpacks](https://github.com/cms-flaf/DSProdGridpacks) under
  `X_HH/MadGraph5_aMCatNLO/13p6TeV/`, mirroring this layout. `ImportGridpack` copies one from
  there; a mass with no stored gridpack is generated from the cards instead. Per-gridpack
  provenance (source file, size, sha256) is documented in each gridpack's own `README.md` there.

## Notes

- **Mass scan:** only the resonance mass changes between points (`__MASS__` → `mass 35` in
  `customizecards.dat`); the width is fixed narrow. The plugin substitutes `__NAME__`/`__MASS__`
  when rendering the cards.
- **Final states share a gridpack:** the Higgses leave MadGraph undecayed, so SL and DL of the same
  mass use one gridpack — the gridpack tasks branch over distinct gridpacks, not points, and it is
  imported (or produced) once.
- **SL vs DL is not just a filter tweak:** the DL fragment additionally enables leptonic `Z` decays
  and `H→ZZ` (`25:onIfMatch = 23 23`), restricts `W`/`Z` to leptonic modes and sets
  `eMuAsEquivalent = off`. Each channel therefore keeps its own McM-sourced fragment rather than a
  generated variant.
