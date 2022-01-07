# python-music-aggregator
Python project to pull data from Spotify, YouTube, and other music streaming platforms for analytics purposes

## Environment Configuration
In order to run any of the Spotify related scripts, you will need a [Spotify developer account](https://developer.spotify.com/) so that you have your own Client ID and Client Secret
- Create a file `env/spotify_credentials.py` with the following variables:
    ```python
    client_id = '<SPOTIFY_CLIENT_ID>'
    client_secret = '<SPOTIFY_CLIENT_SECRET>'
    ```

## Spotify Daemon
