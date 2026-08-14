# X → HH → bb WW (resonant)

Resonant di-Higgs signal: a narrow spin-0 resonance (radion) produced by gluon fusion and
decaying to a pair of Higgs bosons, `gg → X → HH`, with one `H → bb` and one `H → WW`. Points are
a resonance-mass scan; the resonance mass lives in the gridpack, so the gen fragment is common to
all masses.

- **Registered name:** `X_HH_bbWW` (the `process:` key in a DSProd production setup).
- **Generator:** `MadGraph5_aMCatNLO` (LO gridpack) + Pythia8 (CP5) hadronization.

## Layout

```
MadGraph5_aMCatNLO/
├── plugin.py            the ProcessCustomization for this process/generator
└── 13p6TeV/
    ├── cards/           genproductions cards (see cards/README.md for the recipe)
    └── fragment.py      CMSSW gen fragment (Pythia8 CP5 + resonance-decay/final-state filter)
```

## Original sources

- **genproductions recipe** — MadGraph cards follow
  [`cms-sw/genproductions` · `bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0`](https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant),
  template `Radion_hh_narrow_M900`. Details and the per-card breakdown are in
  [`MadGraph5_aMCatNLO/13p6TeV/cards/README.md`](MadGraph5_aMCatNLO/13p6TeV/cards/README.md).
- **Custom model** — `heft_radion`, packaged centrally as `dibosonResonanceModel.tar.gz` and
  fetched by `gridpack_generation.sh` from `cms-project-generators` (referenced in
  `extramodels.dat`); nothing is shipped from this repo.
- **Gen fragment** — derived from the McM request
  [`B2G-Run3Summer22EEwmLHEGS-00612`](https://cms-pdmv.cern.ch/mcm/requests?prepid=B2G-Run3Summer22EEwmLHEGS-00612)
  (single-lepton final state, `2B2JLNu`). The final-state selection is the `ResonanceDecayFilter`
  configured in `fragment.py`.
- **Central gridpacks** — for the standard mass points, existing gridpacks live on cvmfs under
  `/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/.../GF_HH_Spin0/Radion_hh_narrow_M<mass>_*`
  and are imported directly (existing mode); only non-central masses are generated from the cards.

## Notes

- **Mass scan:** only the resonance mass changes between points (`__MASS__` → `mass 35` in
  `customizecards.dat`); the width is fixed narrow. The plugin substitutes `__NAME__`/`__MASS__`
  when rendering the cards.
- **Final state:** the current `fragment.py` selects the single-lepton channel (`2B2JLNu`). The
  gridpack is channel-independent, so alternative final states differ only in the fragment's
  filter — a candidate for a shared `filters/` directory if more channels are added.
