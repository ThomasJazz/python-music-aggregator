# Custom libraries
from lib import method_helper
from lib import spotify_helper
from env import spotify as creds

# Python libraries
import os
import sys
import argparse
import time
from collections import namedtuple

########################################
# ------------------------------------ #
# ------ Variable Configuration ------ #
# ------------------------------------ #
########################################

# Process number info
pid = os.getpid()
print(f'Beginning process with pid={pid}')

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', nargs='*')
parser.add_argument('-rd', '--runduration', nargs='*', default=0)
args_dict = vars(parser.parse_args())
args = namedtuple("Arguments", args_dict.keys())(*args_dict.values())

# General utility functions
helper = method_helper.MethodHelper()

# Spotify API setup
client_id = creds.client_id
client_secret = creds.client_secret
spy = spotify_helper.SpotifyHelper(client_id, client_secret, args.username)

# Frequency to poll users recent songs (in seconds)
poll_frequency = 300 #1500
num_previous = 6

# Output paths
dump_folder = 'dump/'
song_tracker_path = os.path.join(dump_folder, f'{args.username[0]}_song_list.csv')
helper.check_and_create_dir(dump_folder)

# Song history
track_history = None

# For print statements
curr_time = helper.get_sql_date_time()

#########################################
# ------------------------------------- #
# ------------- Functions ------------- #
# ------------------------------------- #
#########################################
def import_previous_songs():
    if (helper.file_exists(song_tracker_path)):
        temp_history = helper.read_csv(song_tracker_path)

        temp_history = helper.convert_2dlst_to_lst_of_dict(temp_history)
        return helper.map_lst_of_dicts_to_dict(temp_history, 'play_hash')
    else:
        helper.write_to_csv(song_tracker_path, [])
        return {}

def dump_data(filename, dataset):
    helper.write_json(os.path.join(dump_folder, filename), dataset)

def get_recent_songs():
    recent_tracks_summary = {}
    recent_tracks = spy.get_recently_played(args.username, num_previous)['items']

    for item in recent_tracks:
        track = item['track']
        track_dict = {
            'track_name': track['name'],
            'track_id': track['id'],
            'artist': track['artists'][0]['name'],
            'artist_id': track['artists'][0]['id'],
            'album': track['album']['name'],
            'album_id': track['album']['id'],
            'duration_ms': track['duration_ms'],
            'played_at': item['played_at']
        }
        play_hash = helper.get_string_hash(str(track_dict))
        track_dict['play_hash'] = play_hash

        recent_tracks_summary[play_hash] = track_dict
        
    return recent_tracks_summary

#########################################
# ------------------------------------- #
# ------------ Script Body ------------ #
# ------------------------------------- #
#########################################

track_history = import_previous_songs()

# Run daemon for amount of time specified in runduration
while (True):
    most_recent = get_recent_songs()
    num_tracks = len(track_history)
    
    print(f'Retrieved latest songs. Filtering new records...')
    
    new_plays = []

    for track_hash in most_recent:
        if not(track_hash in track_history):
            new_plays.append(most_recent[track_hash])
            track_history[track_hash] = most_recent[track_hash]
    
    new_plays = helper.convert_lst_of_dict_to_lst(new_plays)

    try:
        if (num_tracks == 0):
            print(f'\tWriting {len(new_plays)-1} new plays to {song_tracker_path} @ {curr_time}')
            helper.append_to_csv(song_tracker_path, new_plays)
        elif (len(new_plays) > 0):
            print(f'\tWriting {len(new_plays)-1} new plays to {song_tracker_path} @ {curr_time}')
            helper.append_to_csv(song_tracker_path, new_plays[1:])
    except Exception as e:
        print(f'Failed to write to file')

    time.sleep(poll_frequency)
    
