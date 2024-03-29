"""
Module: get_spotify_data.py

This module provides functions to retrieve album information
and track features from the Spotify API.

Dependencies:
- spotipy
- time
- pandas
- numpy
- config (custom module)

Author: Sally Lee
Editor: Eddy Pan

Date: Mar 27, 2024

"""

import time
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import config

# This is the  rate limit per 30 seconds that this code will not exceed
# when making calls to the spotify API
RATE_LIMIT = 80

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def check_rate_limit(times):
    """
    Checks the rate limit and waits if the number of API calls
      exceeds the specified limit.

    Args:
    - times (list): A list containing timestamps of previous API calls.

    Returns:
    - updated_timestamp (list): Updated list of timestamps after considering
      the current API call.
    """
    time_now = time.time()
    times.append(time_now)
    time_thirty_seconds_ago = time_now - 30
    updated_timestamp = [i for i in times if i >= time_thirty_seconds_ago]
    # checks if there have been RATE_LIMIT or more calls
    # to api in last thirty seconds.
    print(
        f"{len(updated_timestamp)} API calls have been made\
              in the last thirty seconds."
    )

    if len(updated_timestamp) >= RATE_LIMIT:
        sleep_time = updated_timestamp[0] - time_thirty_seconds_ago
        print(f"rate limit hit, sleeping for {sleep_time} seconds.")
        # wait a little
        time.sleep(sleep_time)
    return updated_timestamp


def get_album_id(album_name, artist_name, timestamps):
    """
    Retrieve the album ID given the album name and artist name.

    Args:
    - album_name (str): Name of the album.
    - artist_name (str): Name of the artist.
    - timestamps (list): A list containing timestamps of previous API calls.

    Returns:
    - str: Album ID if found, otherwise None.
    """
    # Search for the album
    query = f"album:{album_name} artist:{artist_name}"
    try:
        results = sp.search(q=query, type="album")
    except spotipy.exceptions.SpotifyException:
        time.sleep(30)
        results = sp.search(q=query, type="album")

    timestamps = check_rate_limit(timestamps)
    # Extract album information
    albums = results["albums"]["items"]

    if albums:
        album = albums[
            0
        ]  # Assuming the first search result is the album you want
        album_id = album["id"]
        print("Album Name:", album_name)
        print("Artist Name:", artist_name)
        print("Album ID:", album_id)
        return album_id

    print("Album not found.")
    return None


def get_album_tracks_dataframe(album_name, artist_name, timestamps):
    """
    Retrieve track features of an album and return them as a DataFrame
    Args:
    - album_name (str): Name of the album.
    - artist_name (str): Name of the artist.
    - timestamps (list): A list containing timestamps of previous API calls.

    Returns:
    - pandas.DataFrame: DataFrame containing track features if album is found,
    otherwise None.

    """
    # Get album ID
    album_id = get_album_id(album_name, artist_name, timestamps)
    if album_id:
        # Get album tracks
        try:
            tracks = sp.album_tracks(album_id)["items"]
        except spotipy.exceptions.SpotifyException:
            time.sleep(30)
            tracks = sp.album_tracks(album_id)["items"]

        timestamps = check_rate_limit(timestamps)

        # get track features in batch
        batch_track_ids = [track["id"] for track in tracks]
        try:
            batch_features = sp.audio_features(batch_track_ids)
        except spotipy.exceptions.SpotifyException:
            time.sleep(30)
            batch_features = sp.audio_features(batch_track_ids)
        timestamps = check_rate_limit(timestamps)

        track_features = []
        for features in batch_features:
            track_features.append(features)

        album_tracks_features = []
        for track, features in zip(tracks, track_features):
            track_info = {
                "id": track["id"],
                "track": track["name"],
                "first_artist": track["artists"][0]["name"],
                "all_artists": [artist["name"] for artist in track["artists"]],
                "danceability": features["danceability"],
                "energy": features["energy"],
                "key": features["key"],
                "loudness": features["loudness"],
                "mode": features["mode"],
                "acousticness": features["acousticness"],
                "instrumentalness": features["instrumentalness"],
                "liveness": features["liveness"],
                "valence": features["valence"],
                "tempo": features["tempo"],
                "duration_ms": features["duration_ms"],
                "time_signature": features["time_signature"],
            }
            album_tracks_features.append(track_info)

        # Create DataFrame
        album_features_df = pd.DataFrame(album_tracks_features)
        return album_features_df

    return None
