from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, RadioField, FormField
from wtforms import widgets
from wtforms.validators import DataRequired, Length
from flask_babel import _, lazy_gettext as _l


class BaseForm(FlaskForm):
    submit = SubmitField(_l('Cast Ballot'))


class FPTPForm(FlaskForm):
    ''' Creates fixed entries for FPTP voting system
         - Parties
         - Candidates

    '''
    party = ['Dogs', 'Cats', 'Rabbits', 'Birds']
    candidates = [('sadie', 'S. Sadie'), ('jasper', 'J. Jasper'), \
                            ('fluffy', 'F. Fluffy'), ('isabelle', 'I. Isabelle')]
    cast_vote = RadioField('Parties', choices=candidates)
    submit = SubmitField('Cast Ballot')
    

class MMPForm(FlaskForm):
    ''' Creates fixed entries for MMP voting system
         - Parties
         - Candidates

    '''
    party = ['Dogs', 'Cats', 'Rabbits', 'Birds']
    candidates = [('sadie', 'S. Sadie'), ('jasper', 'J. Jasper'), \
                            ('fluffy', 'F. Fluffy'), ('isabelle', 'I. Isabelle')]
    partymmp = [('dog', 'Dogs'), ('cat', 'Cats'), \
                            ('rabbit', 'Rabbits'), ('bird', 'Birds')]
    candid_vote = RadioField('Parties', choices=candidates)
    party_vote = RadioField('Parties', choices=partymmp)
    submit = SubmitField('Cast Ballot')


class AnimalForm(FlaskForm):
    ''' Creates fixed entries for LPR voting system
         - Parties
         - Candidates
         - Ridings

    '''

    party = ['Dogs', 'Cats', 'Rabbits', 'Birds']
    dog = [('', 'D. Duke'), ('', 'R. Rusty'), \
                 ('', 'T. Tucker'), ('', 'R. Roger')]
    cat = [('', 'S. Shadow'), ('', 'M. Misty'), \
                 ('', 'P. Patch'), ('', 'P. Paws')]
    rabbit = [('', ''), ('', 'C. Clover'), ('', ''), ('', '')]
    bird = [('', 'P. Pikachu'), ('', 'S. Starburst'), \
                  ('', ''), ('', 'F. Flighty')]
    animal = [i[1] for i in dog+cat+rabbit+bird]
    vote_dog = SelectMultipleField('District', choices=dog, 
                            option_widget=widgets.TextInput() )
                          #  widget=widgets.ListWidget(prefix_label=True)
    vote_cat = SelectMultipleField('District', choices=cat, 
                            option_widget=widgets.TextInput() )
                          #  widget=widgets.ListWidget(prefix_label=True)
    vote_rabbit = SelectMultipleField('District', choices=rabbit, 
                            option_widget=widgets.TextInput() )
                          #  widget=widgets.ListWidget(prefix_label=True)     
    vote_bird = SelectMultipleField('District', choices=bird, 
                            option_widget=widgets.TextInput() )
                            
class LPRForm(FlaskForm):
    ''' Combines entries for LPR voting system
        into a single retrievable 'submit' field 

    '''

    vote = FormField(AnimalForm, separator='-')
    submit = SubmitField('Cast Ballot')

class TitleForm(FlaskForm):
    statement = ['Interested in Electoral Reform?', \
                 'Learn how to fill out Proportional Representation Ballots']
    submit = SubmitField('I want to Learn')

class DescriptionForm(FlaskForm):
    statement = ["You'll learn about three ballots?", '* one traditional ballot that is currently in use', "* two other ballots that better represent voter's preferences"]
    submit = SubmitField("Let's do it")

class DirectionsForm(FlaskForm):
    statement = ["For each of three types of ballots there will be:", "* a completed example", "* an empty ballot", "Directions: fill out the empty ballot and get feedback"]
    submit = SubmitField("Let's do it")


'''    
district = [('', 'D. Duke'), ('', 'S. Shadow'), \
                ('', ''), ('', 'P. Pikachu'), \

                ('', 'R. Rusty'), ('', 'M. Misty'), \
                ('', 'C. Clover'), ('', 'S. Starburst'), \

                ('', 'T. Tucker'), ('', 'P. Patch'), \
                ('', ''), ('', ''), \

                ('', 'R. Roger'), ('', 'P. Paws'), \
                ('', ''), ('', 'F. Flighty')]
'''