from app import db, Venue , Artist, Show

venue1 = Venue( "The Musical Hop", "Jazz, Reggae, Swing, Classical, Folk", "1015 Folsom Street", "San Francisco", "CA", "123-123-1234", "https://www.themusicalhop.com","https://www.facebook.com/TheMusicalHop", "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60", True, "We are on the lookout for a local artist to play every two weeks. Please call us.")
venue1.id = 1

venue2 = Venue( "The Dueling Pianos Bar", "Classical, R&B, Hip-Hop", "335 Delancey Street", "New York", "NY", "914-003-1132", "https://www.theduelingpianos.com",  "https://www.facebook.com/theduelingpianos", "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80", False)
venue2.id = 2

venue3 = Venue( "Park Square Live Music & Coffee", "Rock n Roll, Jazz, Classical, Folk", "34 Whiskey Moore Ave", "San Francisco", "CA", "415-000-1234", "https://www.parksquarelivemusicandcoffee.com", "https://www.facebook.com/ParkSquareLiveMusicAndCoffee", "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80", False)
venue3.id = 3

artist1 = Artist("Guns N Petals", "Rock n Roll", "San Francisco", "CA", "326-123-5000", "https://www.gunsnpetalsband.com", "https://www.facebook.com/GunsNPetals",  "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80", True, "Looking for shows to perform at in the San Francisco Bay Area!")
artist1.id = 4

artist2 = Artist("Matt Quevedo", "Jazz", "New York", "NY","300-400-5000","", "https://www.facebook.com/mattquevedo923251523","https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80", False)
artist2.id = 5

artist3 = Artist("The Wild Sax Band", "Jazz, Classical", "San Francisco", "CA", "432-325-5432", "","", "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",False)
artist3.id = 6

db.session.add_all([venue1, venue2, venue3, artist1, artist2, artist3])
db.session.commit()
