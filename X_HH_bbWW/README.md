# X → HH → bb WW (resonant)

Resonant di-Higgs signal: a narrow spin-0 resonance (radion) produced by gluon fusion and
decaying to a pair of Higgs bosons, `gg → X → HH`, with one `H → bb` and one `H → WW`. Points are
a resonance-mass scan; the resonance mass lives in the gridpack, so one fragment per **decay
channel** serves all masses.

- **Registered name:** `X_HH_bbWW` (the `process:` key in a DSProd production setup).
- **Generator:** `MadGraph5_aMCatNLO` (LO gridpack) + Pythia8 (CP5) hadronization.
- **Channels:** `SL` — single lepton (`2B2JLNu`); `DL` — double lepton (`2B2L2Nu`). Each point
  declares one via `channel:`.

## Layout

```
setups/                  production setups (one per era; see below)
MadGraph5_aMCatNLO/
├── plugin.py            the ProcessCustomization for this process/generator
└── 13p6TeV/
    ├── cards/           genproductions cards (see cards/README.md for the recipe)
    └── fragments/
        ├── SL.py        single-lepton gen fragment (2B2JLNu)
        └── DL.py        double-lepton gen fragment (2B2L2Nu)
```

## Production setups

Central production covers only **Run3_2022** and **Run3_2022EE**. The setups here fill the gap:

| Setup | Era | Covers | Samples | Events |
|---|---|---|---|---|
| `setups/Run3_2023_XHHbbWW.yaml` | Run3_2023 | 2023 | 44 (22 masses × SL/DL) | 6.3 M |
| `setups/Run3_2023BPix_XHHbbWW.yaml` | Run3_2023BPix | 2023BPix | 44 | 3.4 M |
| `setups/Run3_2024_XHHbbWW.yaml` | Run3_2024 | 2024 + 2025 + 2026 | 44 | 86.3 M |
| `setups/Run3_XHHbbWW.yaml` | Run3_2022EE | — | 1 (M-800 SL) | 0.1 M |
| `setups/Run3_XHHbbWW_test.yaml` | Run3_2022EE | — | 1 (M-666 SL) | small end-to-end test |

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
  `X_HH/MadGraph5_aMCatNLO/13p6TeV/` — **`X_HH`, not `X_HH_bbWW`**, because the gridpack stops at
  the undecayed HH state and is shared with every other X→HH final state (see
  `gridpack_process` in the plugin). `MakeGridpack` imports from there; a mass with no stored
  gridpack is generated from the cards instead. Per-gridpack provenance (source file, size,
  sha256) is documented in each gridpack's own `README.md` there.

## Notes

- **Mass scan:** only the resonance mass changes between points (`__MASS__` → `mass 35` in
  `customizecards.dat`); the width is fixed narrow. The plugin substitutes `__NAME__`/`__MASS__`
  when rendering the cards.
- **Channels share a gridpack:** the Higgses leave MadGraph undecayed, so SL and DL of the same mass
  use one gridpack — `MakeGridpack` branches over distinct gridpacks, not points, and produces it
  once.
- **SL vs DL is not just a filter tweak:** the DL fragment additionally enables leptonic `Z` decays
  and `H→ZZ` (`25:onIfMatch = 23 23`), restricts `W`/`Z` to leptonic modes and sets
  `eMuAsEquivalent = off`. Each channel therefore keeps its own McM-sourced fragment rather than a
  generated variant.
