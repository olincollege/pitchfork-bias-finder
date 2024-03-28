"""
Module: process_album_data.py

This module defines functions to process album data from CSV files
containing music album information, retrieve audio features of the albums
from the Spotify API, calculate weighted means of various audio features,
and output the processed data to CSV files.

Dependencies:
- pandas
- glob
- time
- get_spotify_data (custom module)

Author: Sally Lee

Date: Mar 27, 2024

"""

import time
import glob
import pandas as pd
from get_spotify_data import get_album_tracks_dataframe


def get_weighted_mean(album_name, artist_name, times):
    """
    Calculate the weighted means of various audio features
    for the tracks in an album.

    Args:
    - album_name (str): Name of the album.
    - artist_name (str): Name of the artist.
    - times (list): A list containing timestamps of previous API calls.

    Returns:
    - pandas.DataFrame: DataFrame containing the weighted means of audio
    features for the album tracks. Returns None if the album is not found.
    """
    album_track_features = get_album_tracks_dataframe(
        album_name, artist_name, times
    )
    if album_track_features is None:
        return None

    weighted_means = {}
    total_duration = album_track_features["duration_ms"].sum()

    for column in album_track_features.columns:
        if (
            column != "id"
            and column != "track"
            and column != "album"
            and column != "first_artist"
            and column != "all_artists"
        ):
            weighted_sum = (
                album_track_features[column]
                * album_track_features["duration_ms"]
            ).sum()
            weighted_means[column] = weighted_sum / total_duration
    # Create a DataFrame for the weighted means
    weighted_means_df = pd.DataFrame(weighted_means, index=[0])
    weighted_means_df["album_name"] = album_name
    weighted_means_df["artist_name"] = artist_name

    # Rearrange columns to have album_name and artist_name at the beginning
    cols = weighted_means_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    weighted_means_df = weighted_means_df[cols]

    return weighted_means_df


def process_album_data(album_row, times):
    """
    Process album data from a row in a DataFrame.

    Args:
    - album_row (pandas.Series): A row from a DataFrame containing album data.
    - times (list): A list containing timestamps of previous API calls.

    Returns:
    - pandas.DataFrame: DataFrame containing the processed album data
      with weighted means of audio features.
    """
    album_name = album_row["album_name"][2:-2]
    artist_name = album_row["artist"][
        2:-2
    ]  # Removing square brackets from artist name
    album_genre = album_row["genre"][
        2:-2
    ]  # Removing square brackets from genre
    rating = float(album_row["rating"][2:-2])
    weighted_means_df = get_weighted_mean(album_name, artist_name, times)
    if weighted_means_df is not None:
        weighted_means_df["genre"] = album_genre
        weighted_means_df["rating"] = rating
        return weighted_means_df


FOLDER_PATH = "pitchfork_data/"

result_dfs = pd.DataFrame(
    columns=[
        "album_name",
        "artist_name",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
        "genre",
        "rating",
    ]
)  # Initialize an empty list to store the results

ALBUM_COUNT = 0
NUMBER = 1


def main():
    """
    Process album data from multiple CSV files in the specified folder.
    This function iterates through each CSV file in the specified folder,
    reads its data, and processes each row using the process_album_data
    function. The processed data is appended to a DataFrame and then
    exported to CSV files based on the genre of the albums.
    """

    timestamps = []
    for file_path in glob.glob(FOLDER_PATH + "*.csv"):
        genre = file_path[len(FOLDER_PATH) : -14]

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            try:
                result = process_album_data(
                    row, timestamps
                )  # Call the function with the current row
                if result is not None:
                    result_dfs = result_dfs._append(  # pylint: disable=W0212
                        result, ignore_index=True
                    )  # Append the result to the list if recognized by spotify

                    ALBUM_COUNT += 1

                    # Check if 300 albums have been processed, if yes, output CSV
                    if ALBUM_COUNT == 300:
                        result_dfs.to_csv(
                            f"spotify_and_pitchfork_data/{genre}_final_{NUMBER}.csv"
                        )
                        result_dfs = pd.DataFrame(
                            columns=result_dfs.columns
                        )  # Reset DataFrame
                        ALBUM_COUNT = 0  # Reset album count
                        NUMBER += 1
            except TypeError:
                pass
            time.sleep(0.2)

        if not result_dfs.empty:
            result_dfs.to_csv(f"spotify_and_pitchfork_data/{genre}_final.csv")


if __name__ == "__main__":
    main()
