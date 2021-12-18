import spotipy as spy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHelper:
    def __init__(self, client_id, client_secret):
        self.spotify = spy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

    # Returns the discography of an artist
    def get_artist_albums(self, artist_id):
        # Build request URI
        artist_uri = f'spotify:artist:{artist_id}'

        results = self.spotify.artist_albums(artist_uri, album_type='album')

        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])

        return albums
    

    def get_artist_albums_summary(self, artist_id):
        album_info = self.get_artist_albums(artist_id)
        summary = []

        for album in album_info:
            name = album['name']
            release_date = album['release_date']
            total_tracks = album['total_tracks']
            artists_in_album = []

            for artist in album['artists']:
                artists_in_album.append(artist['name'])
            
            album_dict = {'name': name, 'release_date': release_date, 'total_tracks': total_tracks, 'artists_in_album': artists_in_album}
            summary.append(album_dict)
        
        return summary