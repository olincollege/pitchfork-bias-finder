"""
test process_album_data
"""

import pytest  # pylint: disable=unused-import
import pandas as pd

from process_album_data import get_weighted_mean, process_album_data


def test_get_weighted_mean():
    """
    Test case for get_weighted_mean function.

    Ensures that the function correctly calculates the
    weighted means of audio features for an album.
    """
    # Test case: valid album data
    album_name = "Rave & Roses"
    artist_name = "Rema"
    timestamps = []
    weighted_mean_df = get_weighted_mean(album_name, artist_name, timestamps)
    assert isinstance(
        weighted_mean_df, pd.DataFrame
    )  # Ensure DataFrame is returned
    assert len(weighted_mean_df) == 1  # Ensure DataFrame has one row
    assert (
        "album_name" in weighted_mean_df.columns
    )  # Ensure album_name column exists
    assert (
        "artist_name" in weighted_mean_df.columns
    )  # Ensure artist_name column exists
    assert (
        "danceability" in weighted_mean_df.columns
    )  # Ensure danceability column exists
    assert "energy" in weighted_mean_df.columns  # Ensure energy column exists
    assert "key" in weighted_mean_df.columns  # Ensure key column exists
    assert (
        "loudness" in weighted_mean_df.columns
    )  # Ensure loudness column exists
    assert "mode" in weighted_mean_df.columns  # Ensure mode column exists
    assert (
        "acousticness" in weighted_mean_df.columns
    )  # Ensure acousticness column exists
    assert (
        "instrumentalness" in weighted_mean_df.columns
    )  # Ensure instrumentalness column exists
    assert (
        "liveness" in weighted_mean_df.columns
    )  # Ensure liveness column exists
    assert "valence" in weighted_mean_df.columns  # Ensure valence column exists
    assert "tempo" in weighted_mean_df.columns  # Ensure tempo column exists
    assert (
        "duration_ms" in weighted_mean_df.columns
    )  # Ensure duration_ms column exists
    assert (
        "time_signature" in weighted_mean_df.columns
    )  # Ensure time_signature column exists


def test_process_album_data():
    """
    Test case for process_album_data function.

    Ensures that the function correctly processes album data
    and returns a DataFrame with the weighted means of audio features.
    """
    # Test case: valid album data
    pitchfork_df = pd.read_csv("pitchfork_data/experimental_pitchfork.csv")
    row = pitchfork_df.iloc[0]

    timestamps = []
    pitchfork_df = process_album_data(row, timestamps)
    assert isinstance(
        pitchfork_df, pd.DataFrame
    )  # Ensure DataFrame is returned
    assert len(pitchfork_df) == 1  # Ensure DataFrame has one row
    assert (
        "album_name" in pitchfork_df.columns
    )  # Ensure album_name column exists
    assert (
        "artist_name" in pitchfork_df.columns
    )  # Ensure artist_name column exists
    assert "genre" in pitchfork_df.columns  # Ensure genre column exists
    assert "rating" in pitchfork_df.columns  # Ensure rating column exists
