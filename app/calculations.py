from app import db
from app.models import FPTPVote, MMPVote, lprvote, LPRRank
from sqlalchemy import and_, or_, not_
import pandas as pd

def riding_results(system, candid, riding, election):
    ''' Calculates the candidate vote totals given a riding, election
        RETURNS: a list of lists, [candidate name, candidate's vote total]

    '''

    tally = []
    for i in candid:
        res = len(system.query.filter(and_(system.election==election,  \
                                    system.riding==riding, system.candid==i)).all())
        tally.append([i, res]) 
    return tally
    

def party_results(system, candid, election):
    ''' Calculates the party vote totals given an election
        Assumes one candidate per party.
        RETURNS: a list [party's vote total]

    '''

    sum_vote = system.query.filter(and_(system.election==election, \
                                     system.candid==candid)).count()
    return sum_vote


def topup_results(system, party, election):
    '''  Calculates the party vote totals given an election
        Uses top-up votes
        RETURNS: a list [party's vote total]
    '''

    sum_vote = system.query.filter(and_(system.election=='Mock Pet Election', \
                                     system.party==party)).count()
    return sum_vote

#def lpr_results(system):
#    df = pd.DataFrame(LPRRank.query.all())
#    df.
