# X → HH (resonant)

Resonant di-Higgs signal: a narrow spin-0 resonance (radion) produced by gluon fusion and decaying
to a pair of Higgs bosons, `gg → X → HH`. Points are a resonance-mass scan; the mass lives in the
gridpack.

**The cards stop at the undecayed HH pair**, which is why the model is called `X_HH` and not after
a production mode or a final state. A point names both, with the tokens the corresponding central
dataset uses **on DAS**:

```yaml
  - name: GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800   # the DAS dataset name
    production_mode: GluGlutoRadion                 # -> cards/GluGlutoRadion/
    final_state: 2B2JLNu                            # -> fragments/2B2JLNu.py
```

Both are open sets, and neither needs code:

- **another final state** = another fragment in `fragments/`, named after its DAS token. It shares
  the cards and the gridpacks, since the decays happen after the generator;
- **another production mode** (VBF, …) = another directory in `cards/` plus one entry in the
  plugin's `PRODUCTION_MODES` (which also holds the gridpack naming of that mode). The fragments,
  the tasks and the gridpack store are unaffected.

- **Registered name:** `X_HH` (the `process:` key in a DSProd production setup).
- **Generator:** `MadGraph5_aMCatNLO` (LO gridpack) + Pythia8 (CP5) hadronization.
- **Production modes shipped:** `GluGlutoRadion` — gluon fusion, narrow spin-0 radion.
- **Final states shipped:** `2B2JLNu` — bbWW single lepton; `2B2L2Nu` — bbWW double lepton.

## Layout

```
setups/                          production setups (one file covers every era)
MadGraph5_aMCatNLO/
├── plugin.py                    the ProcessCustomization for this process/generator
└── 13p6TeV/
    ├── cards/                   genproductions cards, one directory per production mode
    │   └── GluGlutoRadion/      gg -> X(radion) -> HH  (see its README.md for the recipe)
    └── fragments/               one file per final state; the file name IS `final_state:`
        ├── 2B2JLNu.py           bbWW single lepton
        └── 2B2L2Nu.py           bbWW double lepton
```

Both levels use the **DAS tokens** of the corresponding central samples, so a point's `name`,
`production_mode` and `final_state` read the same way as the dataset it reproduces:

```
/GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800/...
 └──────┬──────┘            └──┬───┘
  production_mode            final_state
```

## Production setup

`setups/Run3_XHHbbWW.yaml` — 44 samples (22 masses × 2 final states) for every era central production
misses. **One file for all of them**: `events_total` is given per era, so there is no per-era copy
to keep in sync.

```yaml
  - name: GluGlutoRadiontoHHto2B2Vto2B2JLNu_M-800
    mass: 800
    spin: 0
    final_state: 2B2JLNu
    events_total:
      Run3_2023: 210000
      Run3_2023BPix: 120000
      Run3_2024: 2850000
```

| Era | Covers | Events |
|---|---|---|
| Run3_2023 | 2023 | 6.54 M |
| Run3_2023BPix | 2023BPix | 3.66 M |
| Run3_2024 | 2024 + 2025 + 2026 | 87.06 M |

An era a point does not list simply produces nothing for it. Subsets and short checks are
command-line options of the DSProd tasks (`--points '<glob>'`, `--test <n-events>`), not separate
setups.

**Event targets** start from the central per-mass statistics scaled by integrated luminosity,

```
N(mass, final_state, era) = [ N_2022 + N_2022EE ] / 34664 pb⁻¹ × L(era)
```

with `L` = 17964 pb⁻¹ (2023), 9677 pb⁻¹ (2023BPix) and 246522 pb⁻¹ (2024+2025+2026, which share the
Summer24 MC), and are then **unified over the mass points** in two groups per final state and era:

| era | M ≤ 1000 GeV | M > 1000 GeV |
|---|---|---|
| Run3_2023 | 210 000 | 60 000 |
| Run3_2023BPix | 120 000 | 30 000 |
| Run3_2024 | 2 850 000 | 720 000 |

Each group gets its largest scaled value, rounded up to a multiple of 10 000, so the samples of a
group are directly comparable and no point falls below its luminosity-scaled target. Both final
states end up with the same numbers — their group maxima differed by a single rounding step. The
two groups keep the step the central production itself takes: it used ~11.5 events/pb⁻¹ at low mass
and ~2.9 events/pb⁻¹ high up, so high masses stay proportionally smaller. Unification costs +1.4 %
events overall.

## Original sources

- **genproductions recipe** — MadGraph cards follow
  [`cms-sw/genproductions` · `bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0`](https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant),
  template `Radion_hh_narrow_M900`. Details and the per-card breakdown are in
  [`MadGraph5_aMCatNLO/13p6TeV/cards/README.md`](MadGraph5_aMCatNLO/13p6TeV/cards/README.md).
- **Custom model** — `heft_radion`, packaged centrally as `dibosonResonanceModel.tar.gz` and
  fetched by `gridpack_generation.sh` from `cms-project-generators` (referenced in
  `extramodels.dat`); nothing is shipped from this repo.
- **Gen fragments** — named after their DAS final-state token and taken verbatim from the McM
  requests of the corresponding central samples:
  [`B2G-Run3Summer22EEwmLHEGS-00612`](https://cms-pdmv.cern.ch/mcm/requests?prepid=B2G-Run3Summer22EEwmLHEGS-00612)
  (`2B2JLNu`) and
  [`B2G-Run3Summer22EEwmLHEGS-00656`](https://cms-pdmv.cern.ch/mcm/requests?prepid=B2G-Run3Summer22EEwmLHEGS-00656)
  (`2B2L2Nu`).
- **Central gridpacks** — the standard mass points exist on cvmfs under
  `/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/.../GF_HH_Spin0/Radion_hh_narrow_M<mass>_*`
  and are mirrored into [DSProdGridpacks](https://github.com/cms-flaf/DSProdGridpacks) under
  `X_HH/MadGraph5_aMCatNLO/13p6TeV/GluGlutoRadion/GluGlutoRadiontoHH_M-<mass>/` — **the same levels
  and the same DAS tokens as here**, with `cards/<production_mode>/` on this side matching
  `<production_mode>/` on that one. `ImportGridpack` copies one from there; a mass with no stored
  gridpack is generated from the cards instead. Per-gridpack provenance (source file, size, sha256)
  is documented in each gridpack's own `README.md` there.

## Notes

- **Mass scan:** only the resonance mass changes between points (`__MASS__` → `mass 35` in
  `customizecards.dat`); the width is fixed narrow. The plugin substitutes `__NAME__`/`__MASS__`
  when rendering the cards.
- **Final states share a gridpack:** the Higgses leave MadGraph undecayed, so `2B2JLNu` and
  `2B2L2Nu` of the same mass use one gridpack — the gridpack tasks branch over distinct gridpacks,
  not points, and it is imported (or produced) once. The gridpack **name** comes from the
  production mode (`PRODUCTION_MODES[...]["gridpack"]` → `GluGlutoRadiontoHH_M-800`), so gluon
  fusion and VBF gridpacks stay distinct even where they are stored flat, as they are under a
  production's `<output>/gridpacks/`.
- **`2B2L2Nu` is not just a filter tweak of `2B2JLNu`:** it additionally enables leptonic `Z` decays
  and `H→ZZ` (`25:onIfMatch = 23 23`), restricts `W`/`Z` to leptonic modes and sets
  `eMuAsEquivalent = off`. Each final state therefore keeps its own McM-sourced fragment rather
  than a generated variant.
