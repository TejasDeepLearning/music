from flask import Flask, render_template, send_from_directory, url_for
import os
from PIL import Image

app = Flask(__name__)

# Path to the folder containing your albums
MUSIC_FOLDER = os.path.join('static', 'music')

# Define a standard size for album cover images
COVER_SIZE = (200, 200)

def get_album_cover(album_path):
    """Find and resize the cover image in any format."""
    for file in os.listdir(album_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')):
            cover_path = os.path.join(album_path, file)
            # Open and resize the image
            img = Image.open(cover_path)
            img = img.resize(COVER_SIZE)
            # Save resized cover as a temporary file
            resized_path = os.path.join(album_path, 'cover_resized.jpg')
            img.save(resized_path, format='JPEG')
            return resized_path
    return None  # Return None if no valid cover image is found

# Home route displaying all albums
@app.route('/')
def home():
    # Get album list (subdirectories in the MUSIC_FOLDER)
    albums = []
    for album in os.listdir(MUSIC_FOLDER):
        album_path = os.path.join(MUSIC_FOLDER, album)
        if os.path.isdir(album_path):
            cover_path = get_album_cover(album_path)
            albums.append((album, cover_path))
    return render_template('index.html', albums=albums)

# Route for individual album pages
@app.route('/album/<album_name>')
def album(album_name):
    album_path = os.path.join(MUSIC_FOLDER, album_name)
    songs = [f for f in os.listdir(album_path) if f.endswith(('.mp3', '.wav'))]
    return render_template('album.html', album_name=album_name, songs=songs)

# Serve audio files (both .mp3 and .wav)
@app.route('/music/<album_name>/<song>')
def song(album_name, song):
    return send_from_directory(os.path.join(MUSIC_FOLDER, album_name), song)

if __name__ == '__main__':
    app.run(debug=True)
