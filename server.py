import os
from flask import Flask, render_template, send_file, send_from_directory, redirect, request
from json import JSONDecodeError, JSONEncoder
from flask_mongoengine import MongoEngine
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'ElinoysDB',
    'host': 'localhost',
    'port': 27017,
    'alias': 'default',
    # 'username': 'your_username',
    # 'password': 'your_password'
}

# db = MongoEngine(app)

# class User(UserMixin, db.Document):
#     username = db.StringField(unique=True)
#     password = db.StringField()

movies_folder = './movies'  # Replace with the actual path to your movie files

# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         user = User.objects(username=username).first()
#         if user and user.password == password:
#             login_user(user)
#             return redirect('/')
#         else:
#             return 'Invalid username or password'
#
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/')
# @login_manager.user_loader
# def load_user(user_id):
#     return User.objects(username=user_id).first()

@app.route('/')
# @login_required
def movie_list():
    movie_files = []
    for filename in os.listdir(movies_folder):
        if filename.endswith('.mp4'):
            movie_files.append(filename)
    return render_template('movie_list.html', movies=movie_files)

@app.route('/stream/<filename>')
# @login_required
def stream_movie(filename):
    movie_path = os.path.join(movies_folder, filename)
    return send_file(movie_path, mimetype='video/mp4', conditional=True, etag=True)
#
# @app.route('/movies/<path:filename>')
# @login_required
# def get_movie(filename):
#     return send_from_directory(movies_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
