import model
import movies
from flask import redirect, url_for, render_template, request
from random import randint
from model import Movie
from model import User
from model import Rating
from flask import Flask
app = Flask(__name__)

@app.before_request
def connect():
	db = movies.connect_db("dbh36.mongolab.com", 27367, "movie_user", "password", "movies")
	db = db['movies']
	model.db = db

@app.route("/", methods=["GET"])
def home():
	movie_ids=[]
	ratings=[]
	while len(movie_ids) < 10:
		movie_id = randint(1,1682)
		movie = Movie.get(movie_id)
		movie_ids.append(movie)
		
		movie_id = movie["_id"]
		rating_records = Rating.get_many(movie_id)
		rating = [ rec['rating'] for rec in rating_records ]
		avg = float(sum(rating))/len(rating)
		ratings.append(avg)

	return render_template("potato.html", ratings=ratings, movie_ids=movie_ids)

@app.route("/movie_search/", methods=["POST"])
def search():
	movie_id = int(request.form["search"])
	print movie_id
	# movie = Movie.get(movie_id)
	# return render_template("movie_details.html", movie_id = movie_id)
	return redirect(url_for("movie_details", movie_id=movie_id))
	


@app.route("/movie/<movie_id>", methods=["GET"])
def movie_details(movie_id):
	movie_id = int(movie_id)
	movie = Movie.get(movie_id)
	title = movie["title"]
	genres = movie["genres"]
	genre = ", ".join(genres)
	imdb = movie["imdb_url"]
	movie_id = movie["_id"]
	rating_records = Rating.get_many(movie_id)
	ratings = [ rec['rating'] for rec in rating_records ]
	avg = float(sum(ratings))/len(ratings)
	return render_template("movie_details.html", title=title, genre=genre, avg=avg, imdb=imdb, movie=movie)


# @app.route('/average', method = "GET")
# def average(movie_id):
# 	ratings_records = Rating.get_many(movie_id = movie_id)

# @app.route('/average', method = "POST")
# def print_average():

if __name__ == "__main__":
	app.run(debug=True)
	


# 	def average_rating(movie_id):
#     rating_records = Rating.get_many(movie_id)
#     ratings = [ rec['rating'] for rec in rating_records ]
#     avg = float(sum(ratings))/len(ratings)

#     print "%.2f"%(avg)