import os
import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect, send_file, flash
from pymongo import MongoClient
import gridfs
from bson import ObjectId

from classes.Movie import Movie
from classes.Series import Series
from classes.User import User

app = Flask(__name__)
app.secret_key = 'Elinoy is the best'

client = MongoClient('localhost', 27017)

db = client.ElinoysDB

fs = gridfs.GridFS(db)

users_col = db.Users
movies_col = db.Movies
series_col = db.Series

ALLOWED_VIDEO_EXTENSIONS = {'mp4'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

movies_folder = './movies'  # Replace with the actual path to your movie files

def allowed_movie_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def delete_movie(movie_id):
    fs.delete(movie_id)
    movies_col.delete_one({'video_id': movie_id})

@app.route('/manager/movie/<id>', methods=['GET'])
@app.route('/manager/movie', methods=['GET', 'POST'])
def movie_manager(id=""):
    if 'username' in session:
        logged_user = users_col.find_one({'username': session["username"]})
        if "is_admin" in logged_user and logged_user["is_admin"]:
            if id:
                movie_id = ObjectId(id)
                delete_movie(movie_id)
                flash("Successfully deleted")
                return redirect("/manager/movie")
            if request.method == 'POST':
                if(not request.form['name']):
                    flash('No Name')
                    return redirect(request.url)
                # check if the post request has the file part
                if 'movie' not in request.files:
                    flash('No file part')

                    return redirect(request.url)
                file = request.files['movie']
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    flash('No selected file')

                    return redirect(request.url)
                if file and allowed_movie_file(file.filename):
                    movie = Movie(request.form['name'], fs.put(file))
                    movies_col.insert_one(movie.__dict__)
                    flash('Successfully uploaded')
                    return redirect(request.url)
                flash('incorrect file type')
                return redirect(request.url)
            movies_list = movies_col.find()
            return render_template('upload_movie.html', movies=movies_list)


    return redirect(url_for('home'))

@app.route('/upload-series', methods=['GET', 'POST'])
def upload_series():
    if request.method == 'POST':
        if (not request.form['name']):
            flash('No Name')
            return redirect(request.url)

        episodes = request.files.getlist('series')

        movies_allowed = []
        for i in range(0, len(episodes)):
            movies_allowed.append(allowed_movie_file(episodes[i].filename))

        if episodes and all(movies_allowed) and request.form['name']:

            for i in range(0, len(episodes)):
                episodes[i] = fs.put(episodes[i])

            series = Series(request.form['name'], episodes)

            series_col.insert_one(series.__dict__)

            flash('Successfully uploaded')
            return redirect(request.url)
        flash('incorrect file type')
        return redirect(request.url)
    return render_template('upload_series.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        new_user = User(request.form['username'], bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt()))
        try:
            User(users_col.find_one({'username': new_user.username}))
            flash(new_user.username + ' username already exists')
            return redirect('/signup')
        except:
            new_user.signup()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            existing_user = User(users_col.find_one({'username': request.form['username']}))
            if existing_user.correct_password(request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('movie_list'))
        except:
            pass

        flash('Username and password combination is wrong')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def sign_out():
    session.pop('username')
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list/movie')
def movie_list():
    if 'username' in session:
        movies_list = movies_col.find()
        print(movies_list)

        return render_template('movie_list.html', movies=movies_list)
    return redirect(url_for('login'))

@app.route('/list/series')
def series_list():
    if 'username' in session:
        series_list = series_col.find()
        print(series_list.__dict__)

        return render_template('series_list.html', series_list=series_list)
    return redirect(url_for('login'))

@app.route('/stream/<filename>')
def stream_movie(filename):
    if 'username' in session:
        movie_id = ObjectId(filename)
        video = fs.get(movie_id)
        return send_file(video, mimetype='video/mp4', conditional=True, etag=True)
    return redirect(url_for('login'))
#


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


