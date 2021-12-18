# Custom libraries
from lib import method_helper
from lib import spotify_helper
from env import spotify as creds

# Python libraries
import os
import json
import pprint

########################################
# ------------------------------------ #
# ------ Variable Configuration ------ #
# ------------------------------------ #
########################################

helper = method_helper.MethodHelper()

# Spotify API setup
client_id = creds.client_id
client_secret = creds.client_secret
spy = spotify_helper.SpotifyHelper(client_id, client_secret)

# For readable JSON printing
# Usage: pp.pprint(string)
pp = pprint.PrettyPrinter(indent=4)

# Output paths
dump_path = 'dump/'

# https://open.spotify.com/artist/2V2SmuR8XmWsKjGzTSk6Hp?si=9g0tdCDvTIi6POf-68zWyg
filmmaker_id = '2V2SmuR8XmWsKjGzTSk6Hp'

#########################################
# ------------------------------------- #
# ------------ Script Body ------------ #
# ------------------------------------- #
#########################################

album_data = spy.get_artist_albums(filmmaker_id)
albums_summary = spy.get_artist_albums_summary(filmmaker_id)

# Write files
with open(os.path.join(dump_path, f'{filmmaker_id}_full_data.txt'), 'w') as outfile:
    json.dump(album_data, outfile, indent=4)

with open(os.path.join(dump_path, f'{filmmaker_id}_summarized_data.txt'), 'w') as outfile:
    json.dump(albums_summary, outfile, indent=4)