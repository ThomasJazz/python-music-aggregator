# Custom libraries
from lib import method_helper
from lib import spotify_helper
from env import spotify as creds

# Python libraries
import os
import json
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

########################################
# ------------------------------------ #
# ------ Variable Configuration ------ #
# ------------------------------------ #
########################################
username = '12850397'

# General utility functions
helper = method_helper.MethodHelper()

# Spotify API setup
client_id = creds.client_id
client_secret = creds.client_secret
spy = spotify_helper.SpotifyHelper(client_id, client_secret, username)

# For readable JSON printing
# Usage: pp.pprint(string)
pp = pprint.PrettyPrinter(indent=4)

# Output paths
dump_path = 'dump/'

# https://open.spotify.com/artist/2V2SmuR8XmWsKjGzTSk6Hp?si=9g0tdCDvTIi6POf-68zWyg
filmmaker_id = '2V2SmuR8XmWsKjGzTSk6Hp'

#########################################
# ------------------------------------- #
# ------------- Functions ------------- #
# ------------------------------------- #
#########################################
def dump_data(filename, dataset):
    helper.write_json(os.path.join(dump_path, filename), dataset)

#########################################
# ------------------------------------- #
# ------------ Script Body ------------ #
# ------------------------------------- #
#########################################

#album_data = spy.get_artist_albums(filmmaker_id)
#albums_summary = spy.get_artist_albums_summary(filmmaker_id)
#playlist_data = spy.get_user_playlists('12850397')

# Write files example:
# dump_data('12850397_playlist_full.txt', playlist_data)

#user = spy.get_user('12850397')
#data = spyc.current_user_recently_played(limit=1000)
#data = spy.get_recently_played(username, limit=50)
#albums_summary = spy.get_artist_albums_summary(filmmaker_id)
#artists = spy.get_recently_played_artists(username, 50)
#top_artists = spy.get_user_top_artists(username)

top_artists_long = spy.get_user_top_artists_summary(username, 10)
top_artists_medium = spy.get_user_top_artists_summary(username, 10, 'medium_term')
top_artists_short = spy.get_user_top_artists_summary(username, 10, 'short_term')

dump_data('top_artists_long.txt', top_artists_long)
dump_data('top_artists_medium.txt', top_artists_medium)
dump_data('top_artists_short.txt', top_artists_short)

print('\nShort term favorite artists (last ~4 weeks):')
print(json.dumps(spy.get_artist_names_from_summary(top_artists_short), indent=4))
print('\nMedium term favorite artists: (last ~6 months):')
print(json.dumps(spy.get_artist_names_from_summary(top_artists_medium), indent=4))
print('\nLong term favorite artists: (since account creation):')
print(json.dumps(spy.get_artist_names_from_summary(top_artists_long), indent=4))