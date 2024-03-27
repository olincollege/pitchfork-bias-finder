import spotipy
import time
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import config

# This is the  rate limit per 30 seconds that this code will not exceed when making calls
# to the spotify API
RATE_LIMIT = 5

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def check_rate_limit(times):
    time_now = time.time()
    times.append(time_now)
    time_thirty_seconds_ago = time_now - 30
    y = [i for i in times if i >= time_thirty_seconds_ago]
    # checks if there have been RATE_LIMIT or more calls to api in last thirty seconds.
    print(f"{len(y)} API calls have been made in the last thirty seconds.")

    if len(y) >= RATE_LIMIT:
        sleep_time = y[0] - time_thirty_seconds_ago
        print(f"rate limit hit, sleeping for {sleep_time} seconds.")
        # wait a little
        time.sleep(sleep_time)
    return y


def get_album_id(album_name, artist_name, timestamps):
    # Search for the album
    query = f"album:{album_name} artist:{artist_name}"
    try:
        results = sp.search(q=query, type="album")
    except spotipy.exceptions.SpotifyException:
        time.sleep(0.1)
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
    else:
        print("Album not found.")
        return None


def get_album_tracks_dataframe(album_name, artist_name, timestamps):
    # Get album ID
    album_id = get_album_id(album_name, artist_name, timestamps)
    if album_id:
        # Get album tracks
        try:
            tracks = sp.album_tracks(album_id)["items"]
        except spotipy.exceptions.SpotifyException:
            time.sleep(0.1)
            tracks = sp.album_tracks(album_id)["items"]

        timestamps = check_rate_limit(timestamps)

        # get track features in batch
        batch_track_ids = [track["id"] for track in tracks]
        try:
            batch_features = sp.audio_features(batch_track_ids)
        except spotipy.exceptions.SpotifyException:
            time.sleep(0.1)
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
        df = pd.DataFrame(album_tracks_features)
        return df
    else:
        return None


# print(get_album_tracks_dataframe("Becoming Undone", "ADULT"))


# # Define function to fetch album tracks and their features
# def get_album_tracks_features(album_id):
#     tracks = sp.album_tracks(album_id)["items"]
#     track_ids = [track["id"] for track in tracks]

#     # Fetch track features in batches (max 100 at a time)
#     batch_size = 100
#     track_features = []
#     for i in range(0, len(track_ids), batch_size):
#         batch_track_ids = track_ids[i : i + batch_size]
#         batch_features = sp.audio_features(batch_track_ids)
#         for features in batch_features:
#             track_features.append(features)

#     album_features = []
#     for track in tracks:
#         track_info = {
#             "id": track["id"],
#             "track": track["name"],
#             "first_artist": track["artists"][0]["name"],
#             "all_artists": [artist["name"] for artist in track["artists"]],
#         }
#         track_info.update(get_track_features(track["id"]))
#         # time.sleep(0.1)
#         album_features.append(track_info)
#     return album_features


# def get_album_tracks_dataframe(album_name, artist_name):
#     # Get album ID
#     album_id = get_album_id(album_name, artist_name)
#     if album_id:
#         # Get album tracks features
#         album_tracks_features = get_album_tracks_features(album_id)
#         # Create DataFrame
#         df = pd.DataFrame(album_tracks_features)
#         return df
#     else:
#         # print("Album not found.")
#         return None
