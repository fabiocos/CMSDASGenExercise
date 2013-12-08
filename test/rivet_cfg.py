import FWCore.ParameterSet.Config as cms

process = cms.Process('RIVET')

# import of standard configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:gen.root')                        
)

# Rivet analysis

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('CMS_EWK_10_012','MC_LES_HOUCHES_SYSTEMATICS_CMS')
process.rivetAnalyzer.OutputFile = cms.string('outWanalysis.aida')

process.rivet_step = cms.Sequence(process.rivetAnalyzer)

process.p = cms.Path(process.rivet_step)

