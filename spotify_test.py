import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_album(artist):
    print("going to spotify api")
    # 2WX2uTcsvV5OnS0inACecP
    birdy_uri = 'spotify:artist:'+ artist
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    try:
        results = spotify.artist_albums(birdy_uri, album_type='album')
        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])
        response = []
        for album in albums:
            response.append(album['name'])
        return "success", response
    except spotipy.exceptions.SpotifyException as e:
        if e.code == -1:
            return "Invalid artist id "+artist , []
        return "Spotify api failed", []
    except Exception as e:
        return "Some error occurred - please contact admin", [] 
    