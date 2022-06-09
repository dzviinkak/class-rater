from numpy import average
from web import app, db, forms
from web.models import User
import web.forms as forms
from flask import render_template, session, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from .models import *
from sqlalchemy import func
from werkzeug.urls import url_parse


# saving queries as globals for easier routing
courses = []
reviews = []
chosen_course = {'prompt': 'Choose a course to see or leave reviews!',
  'average_difficulty': 5,
  'average_quality': 5,
  'average_workload': 5,
  'overall': 5}
reviews_detailed = []

# ---- routing ----
@app.route('/')
def index(**kwargs):
  """
      Main page of the web application. Handles cases when the user is logged in and when they are not.
  """
  # check if logged in, i.e. if the session has a saved username
  # not session.get('username')
  if 'username' not in session:
    return render_template('welcome.html')
  else:
    global majors
    majors = db.session.query(Major)
    #try:
    rendered = render_template('index.html', majors=majors, courses=courses,
        reviews=reviews, chosen_course=chosen_course, reviews_detailed=reviews_detailed)
    #except:
    #  return redirect(url_for('index'))

    return rendered

# users
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# TODO figure out the error
@app.route('/login', methods = ['GET','POST'])
def login():
  """
      Login page. It has get and post methods. Dispslays error message if incorrect login data provided.
  """
  # authenticate the user
  #check if user is logged in, if so redirect to a page that makes sense
  if 'username' in session:
    return render_template('index.html', majors = majors)
  form = forms.LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(username = form.username.data).first()
      if not user or not user.check_password(form.password.data):
        flash('Invalid username!')
        return redirect(url_for('login'))

      session['username'] = user.username
      return redirect(url_for('index', majors = majors))
  return render_template("login.html", form=form)


# registration
@app.route('/register', methods=['GET', 'POST'])
def register():
  """
        Sign up pages. Has get and post methods
    """
  form = forms.RegistrationForm(csrf_enabled=False)
  if request.method == 'POST':
    user = db.session.query(User).filter(User.username==request.form['username']).first()
    if not user:
      if form.validate_on_submit():
        # define user with data from form here:
        user = User(username=form.username.data, email=form.email.data)
        # set user's password here:
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        #flash('Login successful')
        return redirect(url_for('index', majors = majors))
    else:
      flash('Please, choose a different username. This one is already taken')
  return render_template("register.html", form = form)

# landing page route
@app.route('/registered_users')
def registered_users():
  # grab all guests and display them
  current_users = User.query.all()
  return render_template('landing_page.html', current_users = current_users)

# showing core courses
@app.route('/show_courses/<major_short_name>/<course_type>')
def show_courses(major_short_name, course_type):
    global courses
    courses = db.session.query(Course)\
      .filter_by(type = course_type)\
      .filter(Course.short_name.contains(major_short_name))

    global reviews
    reviews = db.session.query(Review.course_id,
      func.avg(Review.difficulty).label('average_difficulty'),
      func.avg(Review.quality).label('average_quality'),
      func.avg(Review.workload).label('average_workload'),
      ((func.avg(Review.difficulty) + \
        func.avg(Review.quality) + \
        func.avg(Review.workload))/3).label('overall')
    ).group_by(Review.course_id)

    return redirect(url_for('index'))

@app.route('/select_course/<course_id>')
def show_course_reviews(course_id):
    global chosen_course
    global reviews_detailed

    chosen_course_onclick = db.session.query(Review.course_id,
      func.avg(Review.difficulty).label('average_difficulty'),
      func.avg(Review.quality).label('average_quality'),
      func.avg(Review.workload).label('average_workload'),
      ((func.avg(Review.difficulty) + \
        func.avg(Review.quality) + \
        func.avg(Review.workload))/3).label('overall')
    )\
      .filter_by(course_id = course_id)\
      .group_by(Review.course_id)

    if not chosen_course_onclick.all():
        chosen_course = {'prompt': "The course that you chose doesn't have reviews yet :(",
          'average_difficulty': 5,
          'average_quality': 5,
          'average_workload': 5,
          'overall': 5,
          'course_id': course_id }
    else:
        chosen_course = chosen_course_onclick.first()

    reviews_detailed = db.session.query(
        Review.course_id,
        Review.difficulty,
        Review.quality,
        Review.workload,
        Review.text,
        ((Review.difficulty+Review.quality+Review.workload)/3).label('overall'),
        Review.date
    ).filter_by(course_id = course_id)

    return redirect(url_for('index'))


# leave a review
@app.route('/addreview', methods=['POST'])
def add_review():
    """Add a new review to a specific course.
    It will show in the course page.
    """
    # Note: Will add profs data in the future

    quality = request.form['quality']
    workload = request.form['workload']
    difficulty = request.form['diff']
    text = request.form['review']
    date = datetime.utcnow()

    try:
       cid = chosen_course.course_id
    except:
       cid = chosen_course['course_id']

    new_review = Review(course_id = cid, text = text, difficulty = difficulty, quality = quality, workload = workload, date = date)

    db.session.add(new_review)
    db.session.commit()

    return show_course_reviews(cid)


@app.route('/logout')
def log_out():
    """
        User log out
    """
    # Remove the username from the session
    session.pop('username', None)
    #flash('Logged out successfully!')
    return redirect(url_for('index', majors = majors))


if __name__ == '__main__':
    app.run()