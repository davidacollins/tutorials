from app import app, db
from app.forms import TitleForm, DescriptionForm, DirectionsForm
from app.forms import FPTPForm, MMPForm, LPRForm, AnimalForm
from app.models import Directions, FPTPVote, MMPVote, lprvote, LPRRank
from flask import render_template, redirect
from random import randint
from datetime import datetime
import app.calculations as cal

vv = str(hex(randint(0,999999999)))
riding = ['East Riding', 'South Riding', 'West Riding', 'North Riding']
election = 'Mock Pet Election'
district = 'Happy Valley'

@app.route('/resultsFPTP', methods=['GET', 'POST'])
def resultsFPTP():
    ''' Calculates vote statistics
        Delivers: candidate's vote in each riding
                  total votes in each riding
                  total party votes, across all ridings
                  percentage party votes, across all ridings                  

    '''
    [val, candid] = list(zip(*FPTPForm.candidates))

    # Count winning candidate vote per riding
    k = 0
    win = []  # [riding name, party name, winning candidate, 
              #  winning votes, total votes]
    for i in riding:
        # results is list of lists
        #                    [candidate name, candidate's vote total]
        results = cal.riding_results(FPTPVote, val, i, election)
        winner = sorted(results, key=lambda x: x[1], reverse=True)[0]
        sum_vote = sum(s[1] for s in results)
        idx = val.index(winner[0])
        win.append([i, FPTPForm.party[idx], FPTPForm.candidates[idx][1], winner[1], sum_vote])
        k += 1

    # Count total party votes
    pwin = []  # [party name, total party votes, total party winning %]
    for i in FPTPForm.party:  # make scaleable by zipping lists of FPTPForm.candidates
        idx = FPTPForm.party.index(i)  # then using 'if in'
        candid_value = val[idx] 
        results = cal.party_results(FPTPVote, candid_value, election)
        pwin.append([i, results])
    ptotal = sum(s[1] for s in pwin)
    for i in pwin:
        i.append('{:02.0f}'.format(i[1]/ptotal*100))
    return render_template('fptp_results.html', title='Results', win=win, pwin=pwin)


@app.route('/resultsMMP', methods=['GET', 'POST'])
def resultsMMP():
    ''' Calculates vote statistics
        Delivers: candidate's vote in each riding
                  total votes in each riding
                  total party votes, across all ridings
                  percentage party votes, across all ridings                  

    '''
    [val, candid] = list(zip(*MMPForm.candidates))

    # Count winning candidate vote per riding
    k = 0
    win = []  # [riding name, party name, winning candidate, 
              #  winning votes, total votes]
    for i in riding:
        results = cal.riding_results(MMPVote, val, i, election)
        winner = sorted(results, key=lambda x: x[1], reverse=True)[0]
        sum_vote = sum(s[1] for s in results)
        idx = val.index(winner[0])
        win.append([i, FPTPForm.party[idx], FPTPForm.candidates[idx][1], winner[1], sum_vote])
        k += 1

    # Count total party votes
    # [party name, total party votes, total party winning %]
    pwin = []  # calculated from votes for candidates
    twin = []  # calculated from top-up votes for parties
    for i in MMPForm.party:
        idx = MMPForm.party.index(i)
        candid_value = val[idx] 
        results = cal.party_results(MMPVote, candid_value, election)
        pwin.append([i, results])

    ptotal = sum(s[1] for s in pwin)
    for i in pwin:
        i.append('{:02.0f}'.format(i[1]/ptotal*100))

    [pval, party] = list(zip(*MMPForm.partymmp))
    for i in pval:
        top_results = cal.topup_results(MMPVote, i, election)
        twin.append([i, top_results])

    ttotal = sum(s[1] for s in pwin)
    for i in twin:
        i.append('{:02.0f}'.format(i[1]/ttotal*100))
    return render_template('mmp_results.html', title='Results', win=win, pwin=pwin, twin=twin)

@app.route('/')
@app.route('/index')
def index():
    return 'The tutorial will be right here.  Built today.  Ready this weekend.'


@app.route('/title', methods=['GET'])
def title():
    form = TitleForm()
    redirect('description')
    return render_template('title.html', title='Title', form=form)

@app.route('/description', methods=['GET'])
def description():
    form = DescriptionForm()
    redirect('directions')
    return render_template('description.html', title='Description', form=form)

@app.route('/directions', methods=['GET'])
def directions():
    form = DirectionsForm()
    tempkeys = Directions.query.all()
    keys = [i.voter_key for i in tempkeys]
    global vv
    for key in keys:
        if key == vv:
            vv = str(hex(randint(0,999999999)))
            break 

    voter = Directions(voter_key=vv)
    db.session.add(voter)
    db.session.commit()
    redirect('fptp')
    return render_template('directions.html', title='Directions', form=form)


@app.route('/fptp', methods=['GET', 'POST'])
def fptp():
    ''' Takes data from forms.py
        Reshapes data and sends to fptp.html - incl time spent on page
        Receives votes from fptp.html and adds to database
    '''
    form = FPTPForm()
    party = form.party
    formzip = [list(a) for a in zip(form.party, form.cast_vote)] 
    if form.cast_vote.data != 'None':
        # Calculates time spent on FPTP ballot page
        dt = Directions.query.filter(Directions.voter_key==vv).all()
        deltatime = datetime.utcnow() - dt[0].timestamp
        dlt = str(deltatime.seconds+deltatime.microseconds/1000000)        
        voter = FPTPVote(voter_key=vv, 
                         candid=form.cast_vote.data,
                         riding=riding[randint(0,3)],
                         timestamp=dlt,
                         election=election)
        db.session.add(voter)
        db.session.commit()
        return redirect('mmp')
    return render_template('fptp.html', title='Home', form=form, formzip=formzip, submit=form.submit)


@app.route('/mmp', methods=['GET', 'POST'])
def mmp():
    ''' Takes data from forms.py
        Reshapes data and sends to fptp.html - incl time spent on page
        Receives votes from fptp.html and adds to database
    '''
    form = MMPForm()
    party = form.party
    formzip = [list(a) for a in zip(form.party, form.candid_vote)] 
    if (form.candid_vote.data != 'None') and (form.party_vote.data != 'None'):
        dt = Directions.query.filter(Directions.voter_key==vv).all()
        ft = FPTPVote.query.filter(FPTPVote.voter_key==vv).all()
        temp_time = datetime.utcnow() - dt[0].timestamp 
        dlt = temp_time.total_seconds() - float(ft[0].timestamp)
        voter = MMPVote(voter_key=vv,
                        candid=form.candid_vote.data,
                        riding=riding[randint(0,3)], 
                        party=form.party_vote.data,
                        timestamp=dlt,
                        election=election)
        
        db.session.add(voter)
        db.session.commit()
        return redirect('lpr')
    return render_template('mmp.html', title='Home', form=form, formzip=formzip, submit=form.submit)


@app.route('/lpr', methods=['GET', 'POST'])
def lpr():
    ''' Takes data from forms.py
        Reshapes data and sends to fptp.html - incl time spent on page
        Receives votes from fptp.html and adds to database
    '''
    form = LPRForm() 
    formdata = AnimalForm()
    if (form.vote.vote_dog.data != None) or (form.vote.vote_cat.data != None) \
        or (form.vote.vote_rabbit.data != None) or (form.vote.vote_bird.data != None):
        animal_vote = form.vote.vote_dog.data+form.vote.vote_cat.data+  \
                      form.vote.vote_rabbit.data+form.vote.vote_bird.data
        ssort02 = sorted([i for i in zip(AnimalForm.animal, animal_vote) \
                          if i[1]!=''], key=lambda x: x[1], reverse=False)

        dt = Directions.query.filter(Directions.voter_key==vv).all()
        temp_time = datetime.utcnow() - dt[0].timestamp 
        ft = FPTPVote.query.filter(FPTPVote.voter_key==vv).all()
        mt = MMPVote.query.filter(MMPVote.voter_key==vv).all()
        dlt = temp_time.total_seconds() - float(ft[0].timestamp) \
                                        - float(mt[0].timestamp)
        voter = lprvote(voter_key=vv,
                        riding=riding[randint(0,3)],
                        timestamp=dlt,
                        district=district,
                        election=election)        
        db.session.add(voter)
        db.session.commit()

        l = lprvote.query.filter(lprvote.voter_key==vv).all()
        for i in ssort02:
            ranked = LPRRank()
            ranked.candid=i[0]
            ranked.rank=int(i[1])
            ranked.ballot=l[0]
            db.session.add(ranked)
            db.session.commit()
        return redirect('title')
    return render_template('lpr.html', title='Home', form=form, formdata=formdata)














