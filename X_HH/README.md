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

`setups/Run3_XHHbbWW.yaml` — **160 samples**: the full 40-mass central grid × 2 spin hypotheses
(narrow radion, spin 0; bulk graviton, spin 2) × 2 final states. **One file for all of them**:
`events_total` is given per era, so there is no per-era copy to keep in sync, and **every point
lists every era** — what a given run produces is chosen on the command line.

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

| Era | Covers | NanoAOD | Events as submitted | Storage |
|---|---|---|---|---|
| Run3_2022 | 2022 | v12 | 5.00 M | 26 GB |
| Run3_2022EE | 2022EE | v12 | 14.20 M | 75 GB |
| Run3_2023 | 2023 | v12 | 28.00 M | 148 GB |
| Run3_2023BPix | 2023BPix | v12 | 16.00 M | 85 GB |
| Run3_2024 | 2024 + 2025 + 2026 | v15 | 288.00 M | 1942 GB |
| | | | **351.20 M** | **2.28 TB** |

Storage is at the **measured** NanoAOD size — 5.29 kB/event in v12 and 6.74 in v15, taken from 50
staged nanos merged into one delivered 50 000-event file. (Central NanoAOD on DAS shows
2.9 kB/event, which under-counts these by ~1.8×.) Each version is a full second copy of an era's
events, so the 2022/2023 eras produce **v12 only** — the version central delivers for them —
while 2024 is v15, as its campaign is.

An era a point does not list simply produces nothing for it. Subsets and short checks are
command-line options of the DSProd tasks (`--points '<glob>'`, `--eras`, `--nano-versions`,
`--test <n-events>`), not separate setups — which is why the 2022 restriction below lives in the
command and not in this file.

**Event targets** start from the central per-mass statistics scaled by integrated luminosity,

```
N(mass, final_state, era) = [ N_2022 + N_2022EE ] / 34664 pb⁻¹ × L(era)
```

with `L` = 7990 pb⁻¹ (2022), 26675 pb⁻¹ (2022EE), 17964 pb⁻¹ (2023), 9677 pb⁻¹ (2023BPix) and
246522 pb⁻¹ (2024+2025+2026, which share the Summer24 MC), and are then **unified over the mass
points** in two groups per final state and era:

| era | M ≤ 1000 GeV | M > 1000 GeV |
|---|---|---|
| Run3_2022 | 100 000 | 50 000 |
| Run3_2022EE | 350 000 | 100 000 |
| Run3_2023 | 250 000 | 100 000 |
| Run3_2023BPix | 150 000 | 50 000 |
| Run3_2024 | 2 850 000 | 750 000 |

Each group gets its largest scaled value, rounded up to a whole number of merged files (50 000
events), so the samples of a group are directly comparable, no point falls below its
luminosity-scaled target, and every merged file is full. Both final
states end up with the same numbers — their group maxima differed by a single rounding step. The
two groups keep the step the central production itself takes: it used ~11.5 events/pb⁻¹ at low mass
and ~2.9 events/pb⁻¹ high up, so high masses stay proportionally smaller. Unification costs +1.4 %
events overall.

## Submitting a production

Run the **final** task and LAW schedules everything upstream (`InstallCMSSW` → `ImportGridpack` →
`RunProd` → `NanoMergeTask`). One command per era, from the DSProd checkout after `source env.sh`:

```bash
SETUP=models/X_HH/setups/Run3_XHHbbWW.yaml
```

### Run3_2023, Run3_2023BPix, Run3_2024 — the whole grid

Central production has **nothing** for these eras (verified on DAS: zero `Run3Summer23*`,
`Run3Summer23BPix*` and — for this signal — no 2024 X→HH samples), so all 160 points are produced.

```bash
law run NanoMergeTask --setup $SETUP --eras Run3_2023      --workflow crab
law run NanoMergeTask --setup $SETUP --eras Run3_2023BPix  --workflow crab
law run NanoMergeTask --setup $SETUP --eras Run3_2024      --workflow crab
```

### Run3_2022 and Run3_2022EE — only the masses central lacks

Central already delivers 22 of the 40 masses in both 2022 eras — verified on DAS
(`Run3Summer22*NanoAODv12`, 176 datasets: the same 22 masses for **both** spins and **both** final
states). Producing those again would duplicate a central sample, so a 2022 run is restricted to
the **18-mass gap** — 320, 360, 400, 500, 750, 850, 900, 1100, 1300, 1500, 1700, 1900, 2200, 2400,
2600, 2800, 3500 and 4500 GeV:

```bash
GAP='*_M-320,*_M-360,*_M-400,*_M-500,*_M-750,*_M-850,*_M-900,*_M-1100,*_M-1300,*_M-1500,*_M-1700,*_M-1900,*_M-2200,*_M-2400,*_M-2600,*_M-2800,*_M-3500,*_M-4500'

law run NanoMergeTask --setup $SETUP --eras Run3_2022   --points "$GAP" --workflow crab
law run NanoMergeTask --setup $SETUP --eras Run3_2022EE --points "$GAP" --workflow crab
```

That selects **72 of the 160 points** (18 masses × 2 spins × 2 final states). The globs are
anchored on the mass at the end of the name, so `*_M-500` does not also match `M-5000`.

!!! tip "Check before submitting"
    `--print-status -1` on any of these shows what LAW considers done versus pending without
    running anything, and `--test 100` produces a hundred events per point into `<output>_test`,
    where it cannot touch a production sample.

Swap `--workflow crab` for `htcondor` or `local` — the setup is backend-agnostic. To produce a
single NanoAOD version where the setup lists two, add `--nano-versions v12`; it narrows the
setup's per-era list and never widens it.

## Original sources

- **genproductions recipe** — MadGraph cards follow
  [`cms-sw/genproductions` · `bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0`](https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0),
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
