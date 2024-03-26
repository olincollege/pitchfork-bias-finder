import spotipy
import time
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import config

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_album_id(album_name, artist_name):
    # Search for the album
    query = f"album:{album_name} artist:{artist_name}"
    results = sp.search(q=query, type="album")

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


# Function to fetch track features
def get_track_features(track_id):
    track_info = sp.audio_features(track_id)[0]
    return {
        "danceability": track_info["danceability"],
        "energy": track_info["energy"],
        "key": track_info["key"],
        "loudness": track_info["loudness"],
        "mode": track_info["mode"],
        "acousticness": track_info["acousticness"],
        "instrumentalness": track_info["instrumentalness"],
        "liveness": track_info["liveness"],
        "valence": track_info["valence"],
        "tempo": track_info["tempo"],
        "duration_ms": track_info["duration_ms"],
        "time_signature": track_info["time_signature"],
    }


def get_album_tracks_dataframe(album_name, artist_name):
    # Get album ID
    album_id = get_album_id(album_name, artist_name)
    if album_id:
        # Get album tracks
        tracks = sp.album_tracks(album_id)["items"]
        track_ids = [track["id"] for track in tracks]

        # Fetch track features in batches (max 100 at a time)
        batch_size = 100
        track_features = []
        for i in range(0, len(track_ids), batch_size):
            batch_track_ids = track_ids[i : i + batch_size]
            batch_features = sp.audio_features(batch_track_ids)
            for features in batch_features:
                track_features.append(features)

        # Combine track information with features
        album_tracks_features = []
        for track, features in zip(tracks, track_features):
            track_info = {
                "id": track["id"],
                "track": track["name"],
                "first_artist": track["artists"][0]["name"],
                "all_artists": [artist["name"] for artist in track["artists"]],
            }
            track_info.update(get_track_features(track["id"]))
            album_tracks_features.append(track_info)

        # Create DataFrame
        df = pd.DataFrame(album_tracks_features)
        return df
    else:
        return None


print(get_album_tracks_dataframe("Voyageur", "Ali Farka Touré"))


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
