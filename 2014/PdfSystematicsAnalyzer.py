### NOTE: This is prepared to run on the newest PDFs with LHAPDF >=3.8.4
### so it requires local installation of LHAPDF libraries in order to run 
### out of the box. Otherwise, substitute the PDF sets by older sets

import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("PDFANA")

# Max events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    #input = cms.untracked.int32(10)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(limit = cms.untracked.int32(100)),
            threshold = cms.untracked.string('INFO')
      ),
      destinations = cms.untracked.vstring('cout')
)

# Input files (on disk)
process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring("file:505.0_WToLNu_TuneZ2star_8TeV_pythia6-tauola+WToLNu_TuneZ2star_8TeV_pythia6-tauola+HARVGEN/step1.root")
)

# Produce PDF weights (maximum is 3)
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
      # Fix POWHEG if buggy (this PDF set will also appear on output, 
      # so only two more PDF sets can be added in PdfSetNames if not "")
      # FixPOWHEG = cms.untracked.string("CT10.LHgrid"),
      # GenTag = cms.untracked.InputTag("prunedGenParticles"),
      PdfInfoTag = cms.untracked.InputTag("generator"),
      PdfSetNames = cms.untracked.vstring(
             "CT10.LHgrid"
           , "MSTW2008nlo68cl.LHgrid"
           , "NNPDF21_100.LHgrid"  
      )
)

# Selector and parameters
process.wfilter = cms.EDFilter("MCSingleParticleFilter",
    Status = cms.untracked.vint32(3),
    MaxEta = cms.untracked.vdouble(200.0),
    MinEta = cms.untracked.vdouble(-200.0),
    MinPt = cms.untracked.vdouble(0.0),
    ParticleID = cms.untracked.vint32(24)
)

# Collect uncertainties for rate and acceptance
process.pdfSystematics = cms.EDFilter("PdfSystematicsAnalyzer",
      SelectorPath = cms.untracked.string('pdfana'),
      PdfWeightTags = cms.untracked.VInputTag(
             "pdfWeights:CT10"
           , "pdfWeights:MSTW2008nlo68cl"
           , "pdfWeights:NNPDF21"  
      )
)

# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = cms.untracked.vstring('keep *'),
    fileName = cms.untracked.string('file:pdfana.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pdfana')
    )
)

# Main path
process.pdfana = cms.Path(
       process.pdfWeights
      *process.wfilter
)

process.end = cms.EndPath(process.pdfSystematics+process.RAWSIMoutput)
