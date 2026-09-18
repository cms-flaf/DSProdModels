# X->HH->bbtautau gen fragment, final state 2B2Tau — the file name is the DAS final-state token,
# which is what a setup point asks for with `final_state:`.
# Authoritative source: McM requests/get_fragment/B2G-Run3Summer22EEwmLHEGS-00069, reproduced
# verbatim. Unlike the two bbWW fragments this one needs no `mMin` correction: it restricts no
# W/Z channel, so nothing here can sample a resonance Pythia cannot decay.
#
# The gridpack produces H H (Higgs undecayed); Pythia decays H->bb / H->tautau and the
# ResonanceDecayFilter selects the final state. It is the simplest of the three fragments —
# two channels open on the Higgs, one filter, no Z or W settings at all, and the taus decay
# inclusively. The gridpack is final-state independent, so all three fragments share it.
#
# DSProd's run_step overrides externalLHEProducer.args (the staged gridpack), .nEvents and the
# random seed at the LHEGS step, so this fragment is reused across mass points AND across both
# spins: the M1000 radion tarball below is the one the source request named, not a choice made
# here. Two other requests of the same campaign carry byte-identical processParameters --
# B2G-Run3Summer22EEwmLHEGS-00070 (radion, M-1200) and -00091 (bulk graviton, M-1000), which
# differ from this one only in that tarball path -- and that is what makes one fragment for the
# whole 80-point grid legitimate.

import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13p6TeV/HHresonant/Spin-0

externalLHEProducer = cms.EDProducer(
    "ExternalLHEProducer",
    args=cms.vstring(
        "/cvmfs/cms.cern.ch/phys_generator/gridpacks/RunIII/13p6TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/GF_HH_Spin0/Radion_hh_narrow_M1000_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz"
    ),
    nEvents=cms.untracked.uint32(5000),
    numberOfParameters=cms.uint32(1),
    outputFile=cms.string("cmsgrid_final.lhe"),
    generateConcurrently=cms.untracked.bool(False),
    scriptName=cms.FileInPath(
        "GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh"
    ),
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter(
    "Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint=cms.untracked.int32(1),
    pythiaPylistVerbosity=cms.untracked.int32(1),
    filterEfficiency=cms.untracked.double(1.0),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    comEnergy=cms.double(13600.0),
    PythiaParameters=cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters=cms.vstring(
            "25:m0 = 125.0",
            "25:onMode = off",
            "25:onIfMatch = 5 -5",
            "25:onIfMatch = 15 -15",
            "ResonanceDecayFilter:filter = on",
            "ResonanceDecayFilter:exclusive = on",  # on: require exactly the specified daughters
            "ResonanceDecayFilter:mothers = 25",
            "ResonanceDecayFilter:daughters = 5,5,15,15",
        ),
        parameterSets=cms.vstring(
            "pythia8CommonSettings",
            "pythia8CP5Settings",
            "pythia8PSweightsSettings",
            "processParameters",
        ),
    ),
)

ProductionFilterSequence = cms.Sequence(generator)
