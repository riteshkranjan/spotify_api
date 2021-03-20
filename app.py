from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spotify_test

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def get_album():
    albums = []
    if request.method == 'POST':
        artist = request.form.get("artist")
        album_from_db = db.session.query(Album).filter(Album.artist == artist).all()
        if len(album_from_db) > 0 :
            for album in album_from_db:
                albums.append(album.name)
        else:
            spotify_msg, spotify_albums = spotify_test.get_album(artist)
            if spotify_msg == "success":
                albums += spotify_albums
                for album in albums:
                    a = Album()
                    a.artist = artist
                    a.name = album
                    db.session.add(a)
                    db.session.commit()
            else:
                return render_template('index.html', albums=albums, msg=spotify_msg)
    return render_template('index.html', albums=albums, msg=None)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist = db.Column(db.String(100))
    name = db.Column(db.String(100))

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotify.db'
    db.create_all()
    app.run()