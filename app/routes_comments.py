from app import app, db
from app.forms import TitleForm, DescriptionForm, DirectionsForm
from app.forms import FPTPForm, MMPForm, LPRForm, AnimalForm
from app.models import Directions, FPTPVote, MMPVote, lprvote, LPRRank
from flask import render_template, redirect
from random import randint
from datetime import datetime
import app.calculations as cal

vv = str(hex(randint(0,999999999)))
print(vv)
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
    print('ptotal (fptp) : ', ptotal)
    for i in pwin:
        i.append('{:02.0f}'.format(i[1]/ptotal*100))
    print()
    print()
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
    print('ptotal (mmp) : ', ptotal)
    for i in pwin:
        i.append('{:02.0f}'.format(i[1]/ptotal*100))
    print()
    print()
    print(pwin)

    [pval, party] = list(zip(*MMPForm.partymmp))
    for i in pval:
        top_results = cal.topup_results(MMPVote, i, election)
        twin.append([i, top_results])
    ttotal = sum(s[1] for s in pwin)

    for i in twin:
        i.append('{:02.0f}'.format(i[1]/ttotal*100))
    print()
    print()
    print(twin)

    print('ttotal (mmp) : ', ttotal)
    print()
    print('pwin : ', pwin)
    print('twin : ', twin)
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
  #  try:
    tempkeys = Directions.query.all()
 #   print('KEYS : ', tempkeys)
    keys = [i.voter_key for i in tempkeys]
 #   print('KEYS DATA : ', keys)
    global vv
    for key in keys:
        if key == vv:
            vv = str(hex(randint(0,999999999)))
            break 
 #   except:   
 #   print()
 #   print('vv in Directions : ', vv)
    print()
    voter = Directions(voter_key=vv)
    db.session.add(voter)
    db.session.commit()
    voter = Directions.query.all()
    print('--- Directions ---')
    for d in voter:
        print(d.id, d.voter_key, d.timestamp)   
    
    redirect('fptp')
    return render_template('directions.html', title='Directions', form=form)


@app.route('/fptp', methods=['GET', 'POST'])
def fptp():
    form = FPTPForm()
    party = form.party
    formzip = [list(a) for a in zip(form.party, form.cast_vote)] 
 #   print()
 #   print(form.cast_vote.data)
    if form.cast_vote.data != 'None':
        
 #       voted = FPTPVote(candid=form.cast_vote.data)
 #       print()
 #       print('inside IF :', form.cast_vote.data)
 #       print(FPTPVote.query.all())
 #       print()
        dt = Directions.query.filter(Directions.voter_key==vv).all()
        deltatime = datetime.utcnow() - dt[0].timestamp
        dlt = str(deltatime.seconds+deltatime.microseconds/1000000)
        print()
 #       print('DELTA TIME : ', deltatime)
 #       print(type(deltatime))
 #       print(dlt)
 #       print(type(dlt)) 
        
        voter = FPTPVote(voter_key=vv, 
                         candid=form.cast_vote.data,
                         riding=riding[randint(0,3)],
                         timestamp=dlt,
                         election=election)
        db.session.add(voter)
        db.session.commit()
        voter = FPTPVote.query.all()
        print('--- FPTP ---')
        for d in voter:
            print(d.id, d.voter_key, d.candid, d.riding, d.timestamp, d.election) 
        return redirect('mmp')
    return render_template('fptp.html', title='Home', form=form, formzip=formzip, submit=form.submit)


@app.route('/mmp', methods=['GET', 'POST'])
def mmp():
    form = MMPForm()
    party = form.party
    formzip = [list(a) for a in zip(form.party, form.candid_vote)] 
    print()
#    print(form.candid_vote.data, form.party_vote.data)
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
        voter = MMPVote.query.all()
        print('--- MMP ---')
        for d in voter:
            print(d.id, d.voter_key, d.candid, d.riding, d.timestamp, d.party, d.election) 
        print()
        return redirect('lpr')
    return render_template('mmp.html', title='Home', form=form, formzip=formzip, submit=form.submit)


@app.route('/lpr', methods=['GET', 'POST'])
def lpr():
    form = LPRForm() 
    formdata = AnimalForm()
 #   print(form.vote.vote_dog.data, form.vote.vote_dog.data != None)
 #   print(form.vote.vote_cat.data, form.vote.vote_cat.data != None)
 #   print(form.vote.vote_rabbit.data, form.vote.vote_rabbit.data != None)
 #   print(form.vote.vote_bird.data, form.vote.vote_bird.data != None)
    if (form.vote.vote_dog.data != None) or (form.vote.vote_cat.data != None) \
        or (form.vote.vote_rabbit.data != None) or (form.vote.vote_bird.data != None):
        animal_vote = form.vote.vote_dog.data+form.vote.vote_cat.data+  \
                      form.vote.vote_rabbit.data+form.vote.vote_bird.data
        ssort02 = sorted([i for i in zip(AnimalForm.animal, animal_vote) \
                          if i[1]!=''], key=lambda x: x[1], reverse=False)
        print('ssort02 :', ssort02)

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

        print()
        print('l =', l[0])
        print()
      #  ranked = LPRRank(candid=ssort02[0][0], rank=int(ssort02[0][1]), ballot=l[0])
      #  '''
        for i in ssort02:
            ranked = LPRRank()
            ranked.candid=i[0]
            ranked.rank=int(i[1])
            ranked.ballot=l[0]
            print(ranked)
            db.session.add(ranked)
            db.session.commit()
     #   '''
     #   db.session.add(ranked)
     #   db.session.commit()
        voters = lprvote.query.all()
        print('--- LPR ---')
        for d in voters:
            print(d.id, d.voter_key, d.riding, d.timestamp, d.district, d.election) 
        print()
        return redirect('title')
    return render_template('lpr.html', title='Home', form=form, formdata=formdata)




'''
        {% for vote in form.cast_vote %}
            <tr>
            {% if vote.label != '': %}
                <td>{{ vote }}</td>
                <td>{{ vote.label }}</td>
            {% endif %}
            </tr>
        {% endfor %}
'''
