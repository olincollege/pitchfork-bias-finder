"""
test process_album_data
"""

import pytest
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
    df = get_weighted_mean(album_name, artist_name, timestamps)
    assert isinstance(df, pd.DataFrame)  # Ensure DataFrame is returned
    assert len(df) == 1  # Ensure DataFrame has one row
    assert "album_name" in df.columns  # Ensure album_name column exists
    assert "artist_name" in df.columns  # Ensure artist_name column exists
    assert "danceability" in df.columns  # Ensure danceability column exists
    assert "energy" in df.columns  # Ensure energy column exists
    assert "key" in df.columns  # Ensure key column exists
    assert "loudness" in df.columns  # Ensure loudness column exists
    assert "mode" in df.columns  # Ensure mode column exists
    assert "acousticness" in df.columns  # Ensure acousticness column exists
    assert (
        "instrumentalness" in df.columns
    )  # Ensure instrumentalness column exists
    assert "liveness" in df.columns  # Ensure liveness column exists
    assert "valence" in df.columns  # Ensure valence column exists
    assert "tempo" in df.columns  # Ensure tempo column exists
    assert "duration_ms" in df.columns  # Ensure duration_ms column exists
    assert "time_signature" in df.columns  # Ensure time_signature column exists


def test_process_album_data():
    """
    Test case for process_album_data function.

    Ensures that the function correctly processes album data
    and returns a DataFrame with the weighted means of audio features.
    """
    # Test case: valid album data
    df = pd.read_csv("data/experimental_pitchfork.csv")
    row = df.iloc[0]

    timestamps = []
    df = process_album_data(row, timestamps)
    assert isinstance(df, pd.DataFrame)  # Ensure DataFrame is returned
    assert len(df) == 1  # Ensure DataFrame has one row
    assert "album_name" in df.columns  # Ensure album_name column exists
    assert "artist_name" in df.columns  # Ensure artist_name column exists
    assert "genre" in df.columns  # Ensure genre column exists
    assert "rating" in df.columns  # Ensure rating column exists
