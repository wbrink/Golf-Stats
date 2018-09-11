from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList, SelectField, FormField, SelectMultipleField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ScoreForm9(FlaskForm):
    scores = FieldList(IntegerField('Score'), min_entries=9)
    gir = FieldList(IntegerField('GIR', validators=[NumberRange(min=0, max=1)]), min_entries=9)
    fairway = FieldList(IntegerField('Fairway', validators=[NumberRange(min=0, max=1)]), min_entries=9)
    putts = FieldList(IntegerField('Putts'), min_entries=9)
    tourney = BooleanField("Tournament")
    classifier = RadioField('How Did You Play?', choices=[('very_good','Very Good'), ('good','Good'), ('alright','Alright'), ('bad','Bad'), ('very_bad','Very Bad')], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Length(max=140)])
    submit = SubmitField('Submit')

class ScoreForm18(FlaskForm):
    scores = FieldList(IntegerField('Score'), min_entries=18)
    gir = FieldList(IntegerField('GIR', validators=[NumberRange(min=0, max=1)]), min_entries=18)
    fairway = FieldList(IntegerField('Fairway', validators=[NumberRange(min=0, max=1)]), min_entries=18)
    putts = FieldList(IntegerField('Putts'), min_entries=18)
    tourney = BooleanField("Tournament")
    classifier = RadioField('How Did You Play?', choices=[('Very Good','Very Good'), ('Good','Good'), ('Alright','Alright'), ('Bad','Bad')], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Length(max=140)])
    submit = SubmitField('Submit')

class RoundForm(FlaskForm):
    state = SelectField('State', choices=[('--Select State--','--Select State--'),('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ','NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC','NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')], validators=[DataRequired()], id='select_state')
    course = SelectField('Course', validators=[DataRequired()], id='select_course')
    holes = SelectField('Holes', choices=[('18', '18'),('front_nine', 'Front 9'), ('back_nine', 'Back 9')], validators=[DataRequired()], id='select_holes')
    submit = SubmitField('Submit')

class FilterForm(FlaskForm):
    tourney = SelectField('Tourney', choices=[('All', 'All'),('True', 'Tourney'), ('False', 'Non-Tourney')])
    holes = SelectField('Holes', choices=[('All', 'All'),('True', '9 Holes'), ('False', '18 Holes')])
    #nine_holes = BooleanField('9 Holes')
    #eighteen_holes = BooleanField('18 Holes')
    course = SelectField('Course')
    classifier = SelectField('Level of Play', choices=[('very_good','Very Good'), ('good','Good'), ('alright','Alright'), ('bad','Bad')])
    #date at a later time
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AddCourseForm(FlaskForm):
    state = SelectField('State', choices=[('--Select State--','--Select State--'),('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ','NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC','NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY')], validators=[DataRequired()])
    course_name = StringField('Course', validators=[DataRequired()])
    holes = SelectField('Number of Holes', choices=[('18 Holes', '18 Holes'), ('9 Holes', '9 Holes')])
    submit = SubmitField('Next')

class CourseInfoForm18(FlaskForm):
    par = FieldList(IntegerField('Par'), min_entries=18)
    submit = SubmitField('Submit')

class CourseInfoForm9(FlaskForm):
    par = FieldList(IntegerField('Par'), min_entries=9)
    submit = SubmitField('Submit')



#class FilterForm(FlaskForm):
    #round_filter = SelectField()


#Select fields with dynamic choice values:
#
#class UserDetails(Form):
#    group_id = SelectField(u'Group', coerce=int)
#
#def edit_user(request, id):
#    user = User.query.get(id)
#    form = UserDetails(request.POST, obj=user)
#    form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
