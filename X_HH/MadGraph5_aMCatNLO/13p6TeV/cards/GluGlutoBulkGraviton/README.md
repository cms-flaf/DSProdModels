# Cards: GluGlutoBulkGraviton (gluon fusion, narrow bulk graviton)

The directory name is the **production mode**, in the DAS notation a point uses
(`production_mode: GluGlutoBulkGraviton`). It is the spin-2 sibling of `GluGlutoRadion`: same
`gg -> X -> HH` topology with both Higgs bosons left undecayed, so the two share every fragment,
task and gridpack-store convention, and a point differs only in `production_mode` and `spin`.

Authoritative genproductions recipe
(`cms-sw/genproductions/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-2`,
template `BulkGraviton_hh_GF_HH_narrow_M900`).

- **model**: `RS_bulk_ktilda`, packaged centrally as `dibosonResonanceModel.tar.gz`
  (`extramodels.dat`) — the *same* tarball the radion uses, which packages both models;
  `gridpack_generation.sh` fetches it from `cms-project-generators`. Nothing to ship.
- **process**: `generate p p > y, ( y > H H )` — gg → bulk graviton (`y`, PDG 39) → HH. The radion
  is PDG 35 and `h2`, so the two differ in the resonance field as well as the model.
- **mass scan**: only `mass 39` changes; width fixed narrow (1 MeV). See `customizecards.dat`.
- **run_card**: byte-identical to the radion's — upstream ships the same 13.6 TeV run card for
  both spins, so this is a copy of the one in `../GluGlutoRadion/`.

DSProd renders these per point (`__NAME__` → gridpack name, `__MASS__` → resonance mass) exactly as
for the radion.

**In practice these cards are not used**: central gridpacks exist on cvmfs for every mass in the
setup (`GF_HH_Spin2/BulkGraviton_hh_GF_HH_narrow_M<mass>_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz`),
so the points take the existing-gridpack path. They are here so that a mass without a central
gridpack can still be generated, which is the same arrangement as for the radion.
