#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#Additional imports
from flask_migrate import Migrate
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate (app, db)

# connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# One venue can host many shows --> one-to-many relationship between venues and shows
# One Artist can perform many shows --> one-to-many relationship between artists and shows
# --> An implicit many-to-many relationship between venues and artists

class Venue(db.Model):
  __tablename__ = 'Venue' #I actually tried to change the table name to the non-capitalized form like you suggested. But Lots of errors were raised after doing so. I promise to heed that advice in future applications.

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique = True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  # implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.String(120), default = '')
  website = db.Column(db.String(120), default = '')
  seeking_talent = db.Column(db.Boolean, default =False)
  seeking_description = db.Column(db.String)
  shows = db.relationship('Show', backref= 'venue')

  #A constructor function with arguments used for creating mock data 
  def __init__ (self, name ='', genres ='', address='', city='' , state='', phone='', website='', facebook_link='', image_link='',  seeking_talent = 0 , seeking_description ='', past_shows_count = 0, upcoming_shows_count=0):
    self.name = name
    self.genres = genres
    self.address = address
    self.city = city
    self.state = state
    self.phone = phone
    self.website = website
    self.facebook_link = facebook_link
    self.image_link = image_link
    self.seeking_talent = seeking_talent
    self.seeking_description = seeking_description


class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique = True)
  genres = db.Column(db.String(120), default = '')
  city = db.Column(db.String(120), default = '')
  state = db.Column(db.String(120), default = '')
  phone = db.Column(db.String(120), default = '')
  image_link = db.Column(db.String, default = '')
  facebook_link = db.Column(db.String(120), default = '')

  # implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String(120), default = '')
  seeking_venue = db.Column(db.Boolean, default = False, nullable = False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref= 'artist')

  def __init__ (self, name='', genres='', city='', state='', phone='', website='', facebook_link='', image_link='',   seeking_venue=0 , seeking_description='', past_shows_count=0, upcoming_shows_count=0):
    self.name = name
    self.genres = genres
    self.city = city
    self.state = state
    self.phone = phone
    self.website = website
    self.facebook_link = facebook_link
    self.image_link = image_link
    self.seeking_venue = seeking_venue
    self.seeking_description = seeking_description


# Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show' 

  id = db.Column(db.Integer, primary_key=True)

  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  venue_name = db.Column(db.String)
  venue_image_link = db.Column(db.String(500))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  artist_name = db.Column(db.String)
  artist_image_link = db.Column(db.String)
  start_time = db.Column(db.DateTime)
  
  def __init__ (self, venue_id= -1, venue_name='', venue_image_link='', artist_id = -1, artist_name='', artist_image_link=''):
    self.venue_id = venue_id
    self.venue_name = venue_name
    self.venue_image_link = venue_image_link
    self.artist_id = artist_id
    self.artist_name = artist_name
    self.artist_image_link = artist_image_link

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')



#  Venues
#  --------------------------------------------------------------------------------------------------------------------

@app.route('/venues')
def venues():
  # replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  locations = {}
  venues = Venue.query.all()
  for venue in venues:
    venue_location = (venue.city, venue.state)
    #create a new location if not in locations
    if venue_location not in locations.keys():
        locations[venue_location] = {
          'city': venue.city,
          'state': venue.state,
          'venues': []
        }
    #Add venue to location
    venue_num_upcoming_shows = Show.query.filter(Show.venue_id == venue.id, Show.start_time >= datetime.now()).count()
    locations[venue_location]['venues'].append(
      {'id': venue.id,
      'name':venue.name,
      'num_upcoming_shows': venue_num_upcoming_shows}
    )

  data = locations.values()

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  data = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  count = data.count()
  response={
    "count": count ,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = venue.__dict__ #convert query to dictionary so that we can add more keys
  data['genres'] = list(data['genres'].split(',')) #modify genres to be a list of strings

  #Add show-related-keys

  #I commented out the code that actually worked fine but didn't conform to the rubric and wrote some join queries instead. Don't see a need for a join here since each show object already has all the needed artist and venue data.
  #data['upcoming_shows'] = [show.__dict__ for show in Show.query.filter(Show.venue_id == venue_id, Show.start_time >= datetime.now() )]
  data['upcoming_shows'] = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id, Show.start_time >= datetime.now()).all()
  data['upcoming_shows_count'] = len(data['upcoming_shows'])
  #data['past_shows'] = [show.__dict__ for show in Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now() )]
  data['past_shows'] = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).all()
  data['past_shows_count'] = len(data['past_shows'])

  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  try:
    venue = Venue()
    venue.name = request.form.get('name', '')
    venue.genres = request.form.get('genres', '')
    venue.address = request.form.get('address', '')
    venue.city = request.form.get('city', '')
    venue.state = request.form.get('state', '')
    venue.phone = request.form.get('phone', '')
    venue.facebook_link = request.form.get('facebook_link', '')
      
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET','DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue '+ venue.name + ' was successfully Deleted')
  except:
    flash('Failed deletion attempt')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')






#  Artists
#  --------------------------------------------------------------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')
  data = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  count = data.count()
  response={
    "count": count ,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # replace with real artist data from the artists table, using artist_id
  
  artist = Artist.query.get(artist_id)
  data = artist.__dict__ #convert query to dictionary so that we can add more keys
  data['genres'] = list(data['genres'].split(',')) #modify genres to be a list of strings

  #Again, I commented out the code that actually worked fine but didn't conform to the rubric and wrote some join queries instead. Don't see a need for a join here since each show object already has all the needed artist and venue data.
  #data['upcoming_shows'] = [show.__dict__ for show in Show.query.filter(Show.artist == artist, Show.start_time >= datetime.now() )]
  data['upcoming_shows'] = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time >= datetime.now()).all()
  data['upcoming_shows_count'] = len(data['upcoming_shows'])
  #data['past_shows'] = [show.__dict__ for show in Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now() )]
  data['past_shows'] = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
  data['past_shows_count'] = len(data['past_shows'])

  return render_template('pages/show_artist.html', artist=data)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  try:
    artist = Artist()
    artist.name = request.form.get('name', '')
    artist.genres = request.form.get('genres', '')
    artist.city = request.form.get('city', '')
    artist.state = request.form.get('state', '')
    artist.phone = request.form.get('phone', '')
    artist.facebook_link = request.form.get('facebook_link', '')
      
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')







#  Update
#  --------------------------------------------------------------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj= venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  
  venue.name = request.form.get('name', '')
  venue.genres = request.form.get('genres', '')
  venue.address = request.form.get('address', '')
  venue.city = request.form.get('city', '')
  venue.state = request.form.get('state', '')
  venue.phone = request.form.get('phone', '')
  venue.facebook_link = request.form.get('facebook_link', '')

  db.session.commit()
  
  return redirect(url_for('show_venue', venue_id=venue_id))
  



@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj= artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  
  artist.name = request.form.get('name', '')
  artist.genres = request.form.get('genres', '')
  artist.city = request.form.get('city', '')
  artist.state = request.form.get('state', '')
  artist.phone = request.form.get('phone', '')
  artist.facebook_link = request.form.get('facebook_link', '')

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))







#  Shows
#  --------------------------------------------------------------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  data = Show.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  try:
    show = Show()
    
    show.venue_id = request.form.get('venue_id', '')
    venue = Venue.query.get(show.venue_id)
    show.venue_name = venue.name
    show.venue_image_link = venue.image_link
    
    show.artist_id = request.form.get('artist_id', '')
    artist = Artist.query.get(show.artist_id)
    show.artist_name = artist.name
    show.artist_image_link = artist.image_link
    
    show.start_time = request.form.get('start_time', '')

    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
