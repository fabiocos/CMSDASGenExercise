import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("USER")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'wplusjets.root'
#options.inputFiles = 'file:pythia8ex7.root'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(123456789),
        engineName = cms.untracked.string('HepJamesRandom')
    )
)

process.load('Configuration.EventContent.EventContent_cff')
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string(options.outputFile),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("EmptySource")
#process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.load("CMSDAS2012.GenExercise.WjetsPy6_cff")

# from Configuration.Generator.PythiaUESettings_cfi import *

# #from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *
# process.generator = cms.EDFilter("Pythia6GeneratorFilter",
#     maxEventsToPrint = cms.untracked.int32(5),
#     pythiaPylistVerbosity = cms.untracked.int32(1),
#     filterEfficiency = cms.untracked.double(1.0),
#     pythiaHepMCVerbosity = cms.untracked.bool(False),
#     comEnergy = cms.double(7000.0),
#     PythiaParameters = cms.PSet(
#         pythiaUESettingsBlock,
#         WjetsParameters = cms.vstring('MSEL=0',
#                         'MSUB(1)=1',
#                         '24:ALLOFF',
#                         '24:ONIFMATCH 11 13'),
#         parameterSets = cms.vstring('pythiaUESettings',
#             'WjetsParameters')
#     )
# )
#process.wfilter = cms.EDFilter("MCSingleParticleFilter",
#         Status = cms.untracked.vint32(3),
#     MaxEta = cms.untracked.vdouble(200.0),
#     MinEta = cms.untracked.vdouble(-200.0),
#     MinPt = cms.untracked.vdouble(0.0),
#     ParticleID = cms.untracked.vint32(24)
#)
process.wfilter = cms.EDFilter("MCSingleParticleFilter",
         Status = cms.untracked.vint32(3,3),
     MaxEta = cms.untracked.vdouble(200.0,200.0),
     MinEta = cms.untracked.vdouble(-200.0,-200.0),
     MinPt = cms.untracked.vdouble(0.0,0.0),
     ParticleID = cms.untracked.vint32(24,-24)
)

process.ProductionFilterSequence = cms.Sequence(process.generator)

process.generation_step = cms.Path(process.wfilter)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.generation_step,process.RAWSIMoutput_step)

for path in process.paths:
        getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 
