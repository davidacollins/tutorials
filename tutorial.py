''' This scripts launches the web-based, ballot tutorial app. 
    Available in shell: all databases (FPTP, MMP, LPR)

'''

from app import app, db
from app.forms import FPTPForm
from app.models import Directions, FPTPVote, MMPVote, lprvote, LPRRank
from sqlalchemy.orm import sessionmaker

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Directions': Directions, 'fptp': FPTPForm, 'FPTPVote': FPTPVote, 'MMPVote': MMPVote, 'LPRVote': lprvote, 'LPRRank': LPRRank}
