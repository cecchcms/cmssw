import FWCore.ParameterSet.Config as cms

#------------------------------------ DT ------------------------------------------------
# 1D RecHits
from RecoLocalMuon.DTRecHit.dt1DRecHits_LinearDriftFromDB_cfi import *
# 2D Segments
from RecoLocalMuon.DTSegment.dt2DSegments_MTPatternReco2D_LinearDriftFromDB_cfi import *
# 4D Segments
from RecoLocalMuon.DTSegment.dt4DSegments_MTPatternReco4D_LinearDriftFromDB_cfi import *
# 4D segments with t0 correction
from RecoLocalMuon.DTSegment.dt4DSegments_ApplyT0Correction_cfi import *

#------------------------------------ CSC -----------------------------------------------
# 2D RecHit
from RecoLocalMuon.CSCRecHitD.cscRecHitD_cfi import *
# Segments
from RecoLocalMuon.CSCSegment.cscSegments_cfi import *
from CalibMuon.CSCCalibration.CSCChannelMapper_cfi import *
from CalibMuon.CSCCalibration.CSCIndexer_cfi import *

#------------------------------------ RPC -----------------------------------------------
# 1D RecHits
from RecoLocalMuon.RPCRecHit.rpcRecHits_cfi import *

#----------------------------------------------------------------------------------------
# DT sequence for the standard reconstruction chain 
# The reconstruction of the 2D segments are not required for the 4D segments reconstruction, they are used
# only for debuging purpose and for specific studies
dtlocalreco = cms.Sequence(dt1DRecHits*dt4DSegments + dt1DCosmicRecHits*dt4DCosmicSegments)
# DT sequence with the 2D segment reconstruction
dtlocalreco_with_2DSegments = cms.Sequence(dt1DRecHits*dt2DSegments*dt4DSegments + dt1DCosmicRecHits*dt2DCosmicSegments*dt4DCosmicSegments)
# DT sequence with T0seg correction
# CSC sequence
csclocalreco = cms.Sequence(csc2DRecHits*cscSegments)
# DT, CSC and RPC together
muonlocalreco_with_2DSegments = cms.Sequence(dtlocalreco_with_2DSegments+csclocalreco+rpcRecHits)
# DT, CSC and RPC together (correct sequence for the standard path)
muonlocalreco = cms.Sequence(dtlocalreco+csclocalreco+rpcRecHits)

def _modifyRecoLocalMuonForPhase2( theProcess ):
    theProcess.load("RecoLocalMuon.GEMRecHit.gemRecHits_cfi")
    theProcess.load("RecoLocalMuon.GEMRecHit.me0LocalReco_cff")
    theProcess.muonlocalreco += theProcess.gemRecHits
    theProcess.muonlocalreco += theProcess.me0LocalReco

from Configuration.StandardSequences.Eras import eras
modifyConfigurationStandardSequencesRecoLocalMuonForPhase2_ = eras.phase2_muon.makeProcessModifier( _modifyRecoLocalMuonForPhase2 )
