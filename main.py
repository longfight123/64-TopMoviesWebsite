"""My 'Top Movies' website

This 'Flask' app creates a 'Top Movies' website that the user can
add movies and ratings to. The user also has the ability
to update ratings and reviews for each movie to change
the order that the movies are displayed in. Data is stored inside an SQLite database.

This script requires that 'Flask', 'Flask-SQLAlchemy', 'Flask-WTF',
'Flask-Bootstrap' and 'requests' be installed within the Python
environment you are running this script in.
"""


from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')
try:
    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
except:
    MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')
SEARCH_API_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_DB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'

app = Flask(__name__)
try:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URL_FIXED', 'sqlite:///my-movies.db')
except:
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_FIXED', 'sqlite:///my-movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


class Movies(db.Model):
    """
    A class used to represent a 'Movies' table in a database.
    ...
    Attributes
    ----------
    id: db.Column
        an integer column representing the primary key
    title: db.Column
        a string column representing the title of the movie
    year: db.Column
        a integer column representing the year of release
    description: db.Column
        a string column representing a description of the movie
    rating: db.Column
        a integer column representing the user's rating of the movie
    ranking: db.Column
        a integer column representing the user's personal ranking of the movie
    review: db.Column
        a string column representing the user's personal review of the movie
    img_url: db.Column
        a string column representing a URL to an image of the movie
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(500))
    img_url = db.Column(db.String(500))


try:
    db.create_all()
    movie1 = Movies(id=1,
                    title='千と千尋の神隠し',
                    year=2001,
                    description='A young girl, Chihiro, becomes trapped in a strange new world of spirits. When her parents undergo a mysterious transformation, she must call upon the courage she never knew she had to free her family.',
                    rating=9,
                    ranking=5,
                    review='This was my favorite movie from my childhood.',
                    img_url='https://image.tmdb.org/t/p/w500//39wmItIWsg5sZMyRUHLkWBcuVCM.jpg')
    movie2 = Movies(id=2,
                    title='君の膵臓をたべたい',
                    year=2018,
                    description='Living with Dying." He soon discovers that it is a diary kept by his genuinely cheerful classmate, Sakura Yamauchi, who reveals to him that she is secretly suffering from a pancreatic illness and only has a limited time left.',
                    rating=10,
                    ranking=1,
                    review='This is one of my favorite movies that I\'ve seen in the past decade.',
                    img_url='https://image.tmdb.org/t/p/w500//vHdVU0HyyB6k6kuYt8qjwTz9one.jpg')
    movie3 = Movies(id=3,
                    title='The Martian',
                    year=2015,
                    description='During a manned mission to Mars, Astronaut Mark Watney is presumed dead after a fierce storm and left behind by his crew. But Watney has survived and finds himself stranded and alone on the hostile planet.',
                    rating=8,
                    ranking=4,
                    review='This is a non-stop on the edge of your seat type of movie.',
                    img_url='https://image.tmdb.org/t/p/w500//5BHuvQ6p9kfc091Z8RiFNhCwL4b.jpg')
    movie4 = Movies(id=4,
                    title='Rush Hour',
                    year=1998,
                    description='When Hong Kong Inspector Lee is summoned to Los Angeles to investigate a kidnapping, the FBI doesn\'t want any outside help and assigns cocky LAPD Detective James Carter to distract Lee from the case.',
                    rating=7,
                    ranking=3,
                    review='My favorite comedy featuring one of my favorite actors, Jackie Chan.',
                    img_url='https://image.tmdb.org/t/p/w500//5LM4sJ2SYTvo6q3sOdYaL7Ly3uj.jpg')
    movie5 = Movies(id=5,
                    title='Your Name',
                    year=2018,
                    description='J.J. Abrams and Paramount Pictures have announced they’ll be turning the critically acclaimed Japanese anime Your Name into a live-action film.',
                    rating=9,
                    ranking=2,
                    review='Another amazing movie that came out in the past decade. I highly recommend watching this.',
                    img_url='https://image.tmdb.org/t/p/w500//y00slgxcvchoc7r3bNiI3UbnKkU.jpg')
    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(movie3)
    db.session.add(movie4)
    db.session.add(movie5)
    db.session.commit()
except:
    print('no')
    pass

# new_movie = Movies(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()

class MyForm(FlaskForm):
    """
    A class used to create a Flask-WTForm to update a movies review and rating
    ...
    Attributes
    ----------
    review: StringField
        a string field to submit the user's personal review of a movie
    rating: IntegerField
        an integer field to submit the user's personal rating of the movie
    submit: SubmitField
        a submit field to submit the form
    """
    review = StringField(label='review', validators=[DataRequired(message='Please enter a value.')])
    rating = IntegerField(label='rating', validators=[DataRequired(message='Please enter a value')])
    submit = SubmitField(label='submit')


class AddForm(FlaskForm):
    """
    A class used to create a Flask-WTForm to add a new movie to the website
    ...
    Attributes
    ----------
    title: StringField
        a string field to search for the title of a movie to add
    submit: SubmitField
        a submit field to submit the form
    """
    title = StringField(label='Movie Title', validators=[DataRequired(message='Please enter a value.')])
    submit = SubmitField(label='Submit')

@app.route("/")
def home():
    """the landing page which displays all the user's top movies. The movies appear on the
    landing page in order of the user's personal rating of the movie.

    GET: the landing page
    """
    # Add the order_by() in this order, I'm not sure how to find what order you're actually supposed to do things in
    all_movies = Movies.query.order_by('rating').all()
    i = 1
    for movie in all_movies[::-1]:
        movie.ranking = i
        i += 1
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """a page for the user to update a movie's personal rating and review

    GET: displays the form to edit a movies data
    POST: update the selected movies review and rating, redirect to the landing page
    """
    form = MyForm()
    if form.validate_on_submit():
        movie_id = request.args.get('movie_id')
        new_review = form.review.data
        new_rating = form.rating.data
        selected_movie = Movies.query.get(movie_id)
        selected_movie.review = new_review
        selected_movie.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)

@app.route('/delete')
def delete():
    """a page for the user to delete a movie from the database

    GET: deletes a movie from the database, redirects to the landing page
    """
    movie_id = request.args.get('movie_id')
    selected_movie = Movies.query.get(movie_id)
    db.session.delete(selected_movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """a page for the user to add a new movie to the database

    GET: displays the form to add a new movie
    POST: searches for the movie from an API and redirects the user to a webpage to select the correct
          movie from a list of movies with similar names
    """
    form = AddForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        params = {
            'api_key': MOVIE_API_KEY,
            'query': movie_title,
        }
        response = requests.get(SEARCH_API_URL, params=params)
        response.raise_for_status()
        data = response.json()['results']
        return render_template('select.html', data=data)
    return render_template('add.html', form=form)

@app.route('/new_movie')
def add_new_movie():
    """when the user selects the correct movie to add to the database, the data is obtained from
    an API and added to the database.

    GET: adds the selected movie to a database and redirects the user to the 'edit' page
         to add a personal review and rating of the movie
    """
    movie_id = request.args.get('movie_id')
    params = {
        'api_key': MOVIE_API_KEY
    }
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}', params=params)
    response.raise_for_status()
    data = response.json()
    print(data)
    new_movie = Movies(
        title=data['original_title'],
        year=data['release_date'][0:4],
        description=data['overview'],
        img_url=f'{MOVIE_DB_IMAGE_URL}/{data["poster_path"]}'
    )
    db.session.add(new_movie)
    db.session.commit()
    # Add this line in so we can send the movie_id to the edit route, which is required
    movie = Movies.query.filter_by(title=data['original_title']).first()
    primary_key_id = movie.id
    return redirect(url_for('edit', movie_id=primary_key_id))

if __name__ == '__main__':
    app.run(debug=True)
