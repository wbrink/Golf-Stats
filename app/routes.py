from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, ScoreForm9, ScoreForm18, RoundForm, FilterForm, RegistrationForm, AddCourseForm, CourseInfoForm18, CourseInfoForm9
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Course
import numpy as np
import pandas as pd
import collections
import pygal


##################################
# located at ''/pathname' need to include link in page
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from app import app_dash


course_option = [{'label': i.course, 'value': i.course} for i in Course.query.order_by('course')]
course_option.insert(0, {'label': 'All', 'value': 'All'})

app_dash.layout = html.Div(children=[
    dcc.Dropdown(id='course',
        options=course_option,
        #options.append({'label': 'All', 'value': 'All'}),
        value='All',
        multi=True,
        placeholder="Select a Course"),
    dcc.RadioItems(
        id='holes',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': '9 Holes', 'value': True},
            {'label': '18 Holes', 'value': False}],
        value='All'
        #placeholder="Choose length of round"
    ),
    dcc.Checklist(
        id='tourney',
        options=[
            {'label': 'Tournament', 'value': True},
            {'label': 'Non-Tournament', 'value': False}
        ],
        values=[True, False]
        #labelStyle={'display': 'inline-block'}
    ),

    html.Div(id='my-div')
])


@app_dash.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='course', component_property='value'),
     Input(component_id='holes', component_property='value'),
     Input(component_id='tourney', component_property='values')]
)
def update_output_div(course, holes, tourney):
    if current_user.is_authenticated:
        if (course == 'All' or 'All' in course) and holes == 'All' and False in tourney and True in tourney: #all courses selected
            posts = Post.query.filter_by(user_id=current_user.id).all()
        else: # SQLAlchemy in_ takes a tuple  input_value is a list
            # have to make sure all values are able to be placed in filter
            if holes == 'All':
                holes = (True,False)
            else: #if just one value then need to make tuple for in_
                holes = holes, # this makes it a tuple
            #    return type(holes)
            tourney = tuple(tourney)
            if course == 'All':
                course = [i.course for i in Post.query.filter_by(user_id=current_user.id).all()]

            posts = Post.query.filter(Post.course.in_(tuple(course))).filter(Post.user_id==current_user.id).filter(Post.nine.in_(holes)).filter(Post.tourney.in_(tourney)).all() # need to add in user_id
        if not posts: # query did not work or nothing selected
            return html.H1(children= "Your query doesn't match any results")
        else:
            df = visualizer(posts) # this dataframe has the statistics with dates attached
            return dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': df.date, 'y': df[df.nine==1].score, 'type': 'line', 'name': '9 Holes'}, #nine hole scores
                        {'x': df.date, 'y': df[df.nine==0].score, 'type': 'line', 'name': '18 Holes'},
                    ],
                    'layout':{
                        'title': course,
                        'hovermode': 'closest' #default is compare data on hover

                    }
                }
            )
    else:
        return "You are not currently logged in and cannot view any rounds. Please Login"
#####################################################

"""




@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html')

@app.route('/getting_started')
def getting_started():
    return render_template('getting_started.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: #attribute for every user because of usermixin added to User class
        flash('You are already logged in in as [{}]'.format(current_user.username))
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # returns the user object
        if user is None or not user.check_password(form.password.data): # checks if user is in database or if password matches up
            flash("invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # grabs the redirected page that will be loaded after logging in
        if not next_page or not next_page.startswith('/'): # if no next or does't start with '/' which would mean someone is trying to redirect to somewhere outside the application
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

## User chooses course and amount of holes played
# this route needs to happen before the post so the user picks course and holes played
# this will allow the table to set up in /post with the correct amount of fields
@app.route('/round', methods=['GET', 'POST'])
@login_required
def game():
    form = RoundForm()
    form.course.choices = [(g.course, g.course) for g in Course.query.order_by('course')] # first arg in tuple needs to be string
    if form.validate_on_submit():
        course_name = form.course.data # course chosen
        holes = form.holes.data    # amount of holes played

        return redirect(url_for('post', course_name=course_name, holes=holes))
    return render_template('round.html', form=form)


@app.route('/_get_courses')
def get_courses():
    state = request.args.get('state')

    courses = [row.course for row in Course.query.filter_by(state=state)]
    if courses:
        return jsonify({'course': courses})

    return jsonify({'error': 'No Courses Available'})
    #state = request.args.get('state')

    #courses = [(row.course, row.course) for row in Course.query.filter_by(state=state).all()]
    #if courses:
    #    return jsonify(courses)
    #else:
    #    return jsonify({'error': 'No Courses Available'})



# User enters their stats for the round
@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    # getting variables passed by /round in  url
    holes = request.args.get('holes') # type string
    course_name = request.args.get('course_name') #type string



    if not course_name and not holes:
        flash("need to choose course first")
        return redirect(url_for('index'))
    # query Course table for dictionary of course
    course = Course.query.filter_by(course=course_name).first()
    layout = course.layout # dictionary of hole# and par to be made into dataframe
    if holes == '18' and len(layout['Hole']) < 18:
        flash('This Course only has 9 Holes')
        holes = 'front_nine'
    print(layout)


# setup the course and form fields
    if holes == 'back_nine':
        info = list(layout.values()) # returns list of lists from holes and par
        info = enumerate(list(zip(*info))[9:]) # returns the lis zipped and only 10-18
        layout['Hole'] = layout['Hole'][9:]
        layout['Par'] = layout['Par'][9:]
        form = ScoreForm9()
        eighteen = False
        nine = True
    if holes == 'front_nine':
        info = list(layout.values()) # returns list of lists from holes and par
        info = enumerate(list(zip(*info))[:9]) # returns the lis zipped and only 0-9
        layout['Hole'] = layout['Hole'][:9]
        layout['Par'] = layout['Par'][:9]
        form = ScoreForm9()
        eighteen = False
        nine = True
    if holes == '18':
        info = list(layout.values()) # returns list of lists from holes and par
        info = enumerate(list(zip(*info))) # returns the lis zipped and only 1-18
        form = ScoreForm18()
        eighteen = True
        nine = False

# got the form now validate
    if form.validate_on_submit():
        tourney = form.tourney.data
        scores = form.scores.data       # returns list [] of ints
        fairways = form.fairway.data    # returns list of ints 0 or 1
        gir = form.gir.data             # returns list of ints 0 or 1
        putts = form.putts.data         # returns a list of ints
        total_score = int(sum(scores))
        classifier = form.classifier.data
        notes = form.notes.data

        # creating dictionaries to merge into dataframe
        stats_dict = collections.OrderedDict()
        stats_dict['Hole'] = layout['Hole']
        stats_dict['Par'] = layout['Par']
        stats_dict['Score'] = scores
        stats_dict['GIR'] = gir
        stats_dict['Fairway'] = fairways
        stats_dict['Putts'] = putts

        # making dataframe to place into Post Table
        df = pd.DataFrame(stats_dict) # this is able to take OrderedDict()
        df.loc[df.Par == 3, 'Fairway'] = 0 # this forces fairways to be 0 on par 3s

    # Major stats on the round
    #################################################

        total_putts = df['Putts'].sum()
        total_3putts = df[df.Putts >= 3].shape[0] #gets the number of 3 putts or worse
        fairways_hit = df['Fairway'].sum()
        total_fairways = df[df.Par != 3].shape[0]
        green_hit = df.GIR.sum()
        total_greens = df['GIR'].shape[0]
        score = df['Score'].sum()
        par = df['Par'].sum()
        rel_score = score - par

        # dataframe for birdies, bogies etc.
        df_rel = df['Score'] - df['Par'] # series of relative score
        birdies = df_rel[df_rel == -1].shape[0]
        eagles = df_rel[df_rel == -2].shape[0]
        bogies = df_rel[df_rel == 1].shape[0]
        doubles_or_worse = df_rel[df_rel >= 2].shape[0]

        # a column that will show whether 18 or 9
        if df.shape[0] > 10: # then we know it is 18
            nine = 0
        else:
            nine = 1

        # calculating scrambling percentage of greens missed that result in par or better
        df_scrambling = df[df.GIR == 0]['Score'] - df[df.GIR == 0]['Par']
        successful_scrambling = df_scrambling[df_scrambling <= 0].shape[0]
        attempts_scrambling = df_scrambling.shape[0]


        par5_scoring = df[df.Par == 5]['Score'].sum()
        par5_holes = df[df.Par == 5].shape[0]

            # calculate par 4 scoring
        par4_scoring = df[df.Par == 4]['Score'].sum()
        par4_holes = df[df.Par == 4].shape[0]

            # calculate par 3 scoring
        par3_scoring = df[df.Par == 3]['Score'].sum()
        par3_holes = df[df.Par == 3].shape[0]

            #DataFrame.shape   returns a tupe (# row count, # column count)
        start_scoring = df[0:3]
        start_scoring = start_scoring['Score'] - start_scoring['Par'] # this is now a series
        start_scoring = start_scoring.sum()

        end_scoring = df[-3:]
        end_scoring = end_scoring['Score'] - end_scoring['Par'] # this is now a series
        end_scoring = end_scoring.sum()

        # GIR given fairway hit
        gir_given_fairway = df[df.Fairway == 1]['GIR'].sum()
        gir_given_fairway_total = df[df.Fairway == 1].shape[0]

        # GIR given no fairway hit
        gir_no_fairway_df = df[df.Fairway == 0]
        gir_no_fairway = gir_no_fairway_df[gir_no_fairway_df.Par != 3]['GIR'].sum()
        gir_no_fairway_total = gir_no_fairway_df[gir_no_fairway_df.Par != 3]['GIR'].shape[0]

        # scores given the green was hit
        score_gir = df[df.GIR == 1]['Score'].sum()
        score_gir_par = df[df.GIR == 1]['Par'].sum()
        score_gir_relative = score_gir - score_gir_par

        # GIR for par3s
        gir_par3 = df[df.Par == 3]['GIR'].sum()
        gir_par3_total = df[df.Par == 3]['GIR'].shape[0]

        # post to dictionary
        major_stats_dict = collections.OrderedDict()
        major_stats_dict['par'] = [par]
        major_stats_dict['score'] = [score]
        major_stats_dict['rel_score'] = [rel_score]
        major_stats_dict['birdies'] = [birdies]
        major_stats_dict['eagles'] = [eagles]
        major_stats_dict['bogies'] = [bogies]
        major_stats_dict['doubles_or_worse'] = [doubles_or_worse]
        major_stats_dict['green_hit'] = [green_hit]
        major_stats_dict['total_greens'] = [total_greens]
        major_stats_dict['fairways_hit'] = [fairways_hit]
        major_stats_dict['total_fairways'] = [total_fairways]
        major_stats_dict['total_putts'] = [total_putts]
        major_stats_dict['total_3putts'] = [total_3putts]
        major_stats_dict['par5_scoring'] = [par5_scoring]
        major_stats_dict['par5_holes'] = [par5_holes]
        major_stats_dict['par4_scoring'] = [par4_scoring]
        major_stats_dict['par4_holes'] = [par4_holes]
        major_stats_dict['par3_scoring'] = [par3_scoring]
        major_stats_dict['par3_holes'] = [par3_holes]
        major_stats_dict['start_scoring'] = [start_scoring]
        major_stats_dict['end_scoring'] = [end_scoring]
        major_stats_dict['gir_given_fairway'] = [gir_given_fairway]
        major_stats_dict['gir_given_fairway_total'] = [gir_given_fairway_total]
        major_stats_dict['gir_no_fairway'] = [gir_no_fairway]
        major_stats_dict['gir_no_fairway_total'] = [gir_no_fairway_total]
        major_stats_dict['score_gir_relative'] = [score_gir_relative]
        major_stats_dict['gir_par3'] = [gir_par3]
        major_stats_dict['gir_par3_total'] = [gir_par3_total]
        major_stats_dict['successful_scrambling'] = [successful_scrambling]
        major_stats_dict['attempts_scrambling'] = [attempts_scrambling]
        major_stats_dict['nine'] = [nine]

        df1 = pd.DataFrame(major_stats_dict)


        #Commit to Database in the Post table
        post = Post(stats=df, course=course_name, score=total_score, tourney=tourney, user=current_user,
        eighteen=eighteen, nine=nine, statistics=df1, notes=notes, classifier=classifier)

        db.session.add(post)
        db.session.commit()

        flash(str(total_putts))
        flash(str(par5_scoring))
        flash(str(fairways_hit))
        flash("You shot {}".format(total_score))
        flash("Scores Inputted")
        return redirect(url_for('index'))
    return render_template('post.html', course_info=info, form=form, holes=holes, course_name=course_name)

# gir = list(filter(None.__ne__, gir))      useful for filtering out None values.
# x.__ne__(y) is   x != y
# filter ( function, iterable) if true: returns object with value removed


#function that returns dataframe of scores with date as index
def visualizer(posts): # this needs the queried posts
    df = pd.DataFrame()
    for post in posts:
        if df.empty:
            df = post.statistics
            df = df.assign(date=post.timestamp.strftime('%Y/%m/%d'))
        else:
            df1 = post.statistics
            df1 = df1.assign(date=post.timestamp.strftime('%Y/%m/%d'))
            df = df.append(df1)
    return df


# df['{}'.format(a)]


# lists the posts of the user
@app.route('/my_posts', methods=['GET', 'POST'])
@login_required
def my_posts():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    posts = Post.query.filter_by(user_id=current_user.id).all()
    if not posts:
        flash("There are no posts to be shown")
        return redirect(url_for('index'))

    df = visualizer(posts)
    line_chart = pygal.Line()
    line_chart.title = 'Scores Trend'
    line_chart.x_labels = map(str, list(df.date))
    line_chart.add('9 Holes', list(map(int, df[df.nine == 1]['score'])))
    line_chart.add('18 Holes', list(map(int, df[df.nine != 1]['score'])))
    line_chart = line_chart.render_data_uri()


    form = FilterForm()
    #form.tourney.choices.insert(0,('',''))
    #form.holes.choices.insert(0,('',''))
    form.course.choices = [(g.course, g.course) for g in Course.query.order_by('course')]
    form.course.choices.insert(0, ('All','All')) # inserting choice for nothing
    form.classifier.choices.insert(0,('All','All'))
    if form.validate_on_submit():
        tourney = form.tourney.data
        holes = form.holes.data
        course = form.course.data
        classifier = form.classifier.data

        flash('Filter set')
        return redirect(url_for('allrounds', tourney=tourney, holes=holes, course=course, classifier=classifier))

    return render_template('my_posts.html', posts=posts, form=form, line_chart=line_chart)

# this will show all the rounds and their stats
@app.route('/allrounds')
@login_required
def allrounds(): # could implement a filter that is passed to url

    tourney = request.args.get('tourney')
    holes = request.args.get('holes')
    #nine = request.args.get('nine_holes')
    #eighteen = request.args.get('eighteen_holes')
    course = request.args.get('course')
    classifier = request.args.get('classifier')

    flash(tourney)
    flash(holes)
    flash(course)
    flash(classifier)
    # because requests are passed as strings
#    tourney = eval(tourney)
#    nine = eval(nine)
#    eighteen = eval(eighteen)

    if tourney == 'All': # defaults to all
        tourney = (True,False)
    else:
        tourney = (eval(tourney),)

    if holes == 'All': # defaults to all
        holes = (True,False) # for nine_holes in database; True means that nine holes was chosen
    else:
        holes = (eval(holes),)

    if course == 'All':
        course = [g.course for g in Course.query.all()]
        course = tuple(course)
    else:
        course = (course,)

    if classifier == 'All':
        classifier = ()



    posts = Post.query.filter_by(user_id=current_user.id).all()


    if not posts:
        flash("No rounds to show. Please post a round to view stats")
        return redirect(url_for('index'))
    df = pd.DataFrame()
    counter = 0 # this will give the number of rounds in easy to read way
    for post in posts:
        counter = counter + 1
        if df.empty:
            df = post.statistics
        else:
            df = df.append(post.statistics, ignore_index=False)

    # dataframe for 9 hole stats
    nine = df[df.nine == 1]

    # dataframe for 18 hole stats
    eighteen = df[df.nine == 0]

    # greens hit
    a = [df['green_hit'].sum(), df['total_greens'].sum()]
    gir = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    # scrambling
    a = [df['successful_scrambling'].sum(), df['attempts_scrambling'].sum()]
    scrambling = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    # fairways
    a = [df['fairways_hit'].sum(), df['total_fairways'].sum()]
    fwy = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    #putts per 9
    pp_nine = nine['total_putts'].sum() / nine.shape[0]
    three_putts_9 = nine['total_3putts'].sum() / nine.shape[0]

    #putts per 18
    pp_18 = eighteen['total_putts'].sum() / eighteen.shape[0]
    three_putts_18 = eighteen['total_3putts'].sum() / eighteen.shape[0]

    # eagles per hole
    total_holes = (nine.shape[0]*9) + (eighteen.shape[0]*18)
    eagle_per_hole = total_holes / df['eagles'].sum()
    if df['eagles'].sum() == 0:
        eagle_per_hole = np.nan
    # birdies per 9 and bogies doubles or worse
    birdies_9 = nine['birdies'].sum() / nine.shape[0]
    bogies_9 = nine['bogies'].sum() / nine.shape[0]
    double_worse_9 = nine['doubles_or_worse'].sum() / nine.shape[0]

    #birdies per 18 and bogies dourbles or worse
    birdies_18 = eighteen['birdies'].sum() / eighteen.shape[0]
    bogies_18 = eighteen['bogies'].sum() / eighteen.shape[0]
    double_worse_18 = eighteen['doubles_or_worse'].sum() / eighteen.shape[0]

    # par 5,4,3 Scoring
    par5 = df['par5_scoring'].sum() / df['par5_holes'].sum()
    par4 = df['par4_scoring'].sum() / df['par4_holes'].sum()
    par3 = df['par3_scoring'].sum() / df['par3_holes'].sum()

    # Start (First three holes)
    start_avg = df['start_scoring'].sum() / df.shape[0]
    end_avg = df['end_scoring'].sum() / df.shape[0]

    # gir given fairway hit
    a = [df['gir_given_fairway'].sum(), df['gir_given_fairway_total'].sum()]
    gir_frwy = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    # gir given fairway hit
    a = [df['gir_no_fairway'].sum(), df['gir_no_fairway_total'].sum()]
    gir_no_frwy = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    # score relative to par given gir
    rel_score_gir = df['score_gir_relative'].sum() / df.shape[0]

    #under and over par Rounds
    under_par_rounds = df[df.rel_score < 0].shape[0]
    over_par_rounds = df[df.rel_score > 0].shape[0]
    total_rounds = df.shape[0]
    total_score = df['rel_score'].sum()

    #gir on par3
    a = [df['gir_par3'].sum(), df['gir_par3_total'].sum()]
    gir_par3 = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))



    df_for_show = df.copy() # have to make copy or else original will be edited as well
    df_for_show = df_for_show.to_html(index=True)


    return render_template('allrounds.html', df_for_show=df_for_show, gir=gir, scrambling=scrambling, fwy=fwy, pp_nine=pp_nine, pp_18=pp_18,
    eagle_per_hole=eagle_per_hole, birdies_9=birdies_9, bogies_9=bogies_9, double_worse_9=double_worse_9,
    birdies_18=birdies_18, bogies_18=bogies_18, double_worse_18=double_worse_18, three_putts_9=three_putts_9,
    three_putts_18=three_putts_18, par5=par5, par4=par4, par3=par3, start_avg=start_avg, end_avg=end_avg,
    gir_frwy=gir_frwy, gir_no_frwy=gir_no_frwy, rel_score_gir=rel_score_gir,under_par_rounds=under_par_rounds,
    over_par_rounds=over_par_rounds, total_rounds=total_rounds, total_score=total_score, gir_par3=gir_par3)



# Viewing single round
@app.route('/view_round/<int:id>')
@login_required
def view_round(id):

    user = current_user
    post = Post.query.get(id)

    df = post.stats
    classifier = post.classifier
    notes = post.notes
    course = post.course

    df_for_show = df.copy() # have to make copy or else original will be edited as well
    df_for_show.loc[df.Par==3, 'Fairway']= 'N/A'

    par = df.Par.sum()
    score = df.Score.sum()
    rel_score = score - par
    if rel_score > 0:
        rel_score = '+{}'.format(rel_score)
    score = "{} ({})".format(score, rel_score)

    # calculate fairways hit
    numerator = df.Fairway.sum()
    denominator = df[df.Par != 3]['Fairway'].count() # without Fairway it counts all columns and lists their counts
    fairways = [numerator, denominator]
    fairways_summary = "{}/{} or {}%".format(fairways[0], fairways[1], round((fairways[0]/fairways[1] * 100), 2))

    # calculate gir
    numerator = df.GIR.sum()
    denominator = df['GIR'].count()
    gir = [numerator, denominator]
    gir_summary = "{}/{} or {}%".format(gir[0], gir[1], round((gir[0]/gir[1] * 100), 2))

    # calculating scrambling percentage of greens missed that result in par or better
    df_scrambling = df[df.GIR == 0]['Score'] - df[df.GIR == 0]['Par']
    successful_scrambling = df_scrambling[df_scrambling <= 0].shape[0]
    attempts_scrambling = df_scrambling.shape[0]
    a = [successful_scrambling, attempts_scrambling]
    scrambling = '{}/{} or {}%'.format(a[0], a[1], round((a[0]/a[1])*100, 2))

    # calculate Putts
    putts = df['Putts'].sum()

    # calculate par 5 scoring
    par5_scoring = df[df.Par == 5]
    par5_scoring = par5_scoring['Score'] - par5_scoring['Par'] # this is now a series
    par5_scoring = par5_scoring.sum()
    print(par5_scoring)

    # calculate par 4 scoring
    par4_scoring = df[df.Par == 4]
    par4_scoring = par4_scoring['Score'] - par4_scoring['Par'] # this is now a series
    par4_scoring = par4_scoring.sum()
    print(par4_scoring)

    # calculate par 3 scoring
    par3_scoring = df[df.Par == 3]
    par3_scoring = par3_scoring['Score'] - par3_scoring['Par'] # this is now a series
    par3_scoring = par3_scoring.sum()
    print(par3_scoring)

    #DataFrame.shape   returns a tupe (# row count, # column count)
    start_scoring = df[0:3]
    start_scoring = start_scoring['Score'] - start_scoring['Par'] # this is now a series
    start_scoring = start_scoring.sum()
    print(start_scoring)

    end_scoring = df[-3:]
    end_scoring = end_scoring['Score'] - end_scoring['Par'] # this is now a series
    end_scoring = end_scoring.sum()
    print(end_scoring)

    # GIR given fairway hit
    gir_given_fairway = df[df.Fairway == 1]
    numerator = gir_given_fairway.GIR.sum()
    denominator = gir_given_fairway['GIR'].count()
    gir_given_fairway = [numerator, denominator]
    gir_given_fairway = "{}/{} or {}%".format(gir_given_fairway[0], gir_given_fairway[1], round((gir_given_fairway[0]/gir_given_fairway[1] * 100), 2))


    # GIR given no fairway hit
    gir_no_fairway = df[df.Fairway == 0]
    gir_no_fairway = gir_no_fairway[gir_no_fairway.Par != 3]
    numerator = gir_no_fairway.GIR.sum()
    denominator = gir_no_fairway['GIR'].count()
    gir_no_fairway = [numerator, denominator]
    gir_no_fairway = "{}/{} or {}%".format(gir_no_fairway[0], gir_no_fairway[1], round((gir_no_fairway[0]/gir_no_fairway[1] * 100), 2))

    # scores given the green was hit
    score_gir = df[df.GIR == 1]
    score_par_list = [score_gir['Score'].sum(), score_gir['Par'].sum()] # list [score, par]
    score_gir = score_par_list[0] - score_par_list[1]

    # GIR for par3s
    gir_par3 = df[df.Par == 3]
    numerator = gir_par3.GIR.sum()
    denominator = gir_par3.shape[0]
    gir_par3 = [numerator, denominator]
    gir_par3 = "{}/{} or {}%".format(gir_par3[0], gir_par3[1], round((gir_par3[0]/gir_par3[1] * 100), 2))

    df_rel = df['Score'] - df['Par'] # series of relative score
    birdies = df_rel[df_rel == -1].shape[0]
    eagles = df_rel[df_rel == -2].shape[0]
    bogies = df_rel[df_rel == 1].shape[0]
    doubles_or_worse = df_rel[df_rel >= 2].shape[0]


    df_for_show = df_for_show.to_html(index=False)


    return render_template('view_round.html',df_for_show=df_for_show, course=course, gir=gir_summary, scrambling=scrambling, putts=putts,
    fairways=fairways_summary, par5s=par5_scoring, par4s=par4_scoring, par3s=par3_scoring, par=par, score=score,
    gir_given_fairway=gir_given_fairway, gir_no_fairway=gir_no_fairway, score_gir=score_gir, start_scoring=start_scoring,
    end_scoring=end_scoring, gir_par3=gir_par3, birdies=birdies, eagles=eagles, bogies=bogies, doubles_or_worse=doubles_or_worse,
    classifier=classifier, notes=notes)


# being able to add course
@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        state = form.state.data
        course_name = form.course_name.data
        holes = form.holes.data

        return redirect(url_for('course_info', holes=holes, course_name=course_name, state=state))
    return render_template('add_course.html', form=form)

@app.route('/course_info', methods=['GET','POST'])
@login_required
def course_info():
    state = request.args.get('state')
    holes = request.args.get('holes')
    course_name = request.args.get('course_name')
    if holes == '18 Holes':
        form  = CourseInfoForm18()
        hole_numbers = [i for i in range(18)] # using this to increment throught the FieldList in CourseInfoForm_
    else:
        form = CourseInfoForm9()
        hole_numbers = [i for i in range(9)]

    if form.validate_on_submit():
        par = form.par.data       # returns list [] of ints

        hole_numbers = [i+1 for i in hole_numbers]
        layout = {'Hole': hole_numbers, 'Par': par}

        course = Course(course=course_name, layout=layout, state=state)
        db.session.add(course)
        db.session.commit()

        flash('Course Added')

        return redirect(url_for('index'))

    return render_template('course_info.html', form=form, hole_numbers=hole_numbers)
