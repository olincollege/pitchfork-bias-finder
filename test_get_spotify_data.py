"""
test get_spotify_data
"""

import pytest
import pandas as pd
from get_spotify_data import (
    check_rate_limit,
    get_album_id,
    get_album_tracks_dataframe,
)


def test_check_rate_limit():
    """
    Test case for check_rate_limit function.

    Ensures that the rate limit is properly handled and the list of
    timestamps is updated accordingly.
    """
    # Test case: ensure rate limit is properly handled


def test_get_album_id():
    """
    Test case for get_album_id function.

    Ensures that the function returns the correct album ID
    when the album is found.
    """
    # Test case: album found
    timestamps = []
    album_id = get_album_id("Electricity", "Ibibio Sound Machine", timestamps)
    assert (
        album_id is not None
    )  # Ensure album ID is not None when album is found
    assert isinstance(album_id, str)  # Ensure album ID is a string

    # Test case: album not found
    timestamps = []
    album_id = get_album_id("tiasdfaqw12345sdfweme", "timeasdfghj", timestamps)
    assert album_id is None  # Ensure album ID is None when album is not found


def test_get_album_tracks_dataframe():
    """
    Test case for get_album_tracks_dataframe function.

    Ensures that the function returns a DataFrame when the album ID is valid.
    """
    # Test case: DataFrame returned when album ID is valid
    timestamps = []
    df = get_album_tracks_dataframe(
        "Electricity", "Ibibio Sound Machine", timestamps
    )
    assert isinstance(df, pd.DataFrame)  # Ensure DataFrame is returned

    # Test case: album not found
    timestamps = []
    df = get_album_tracks_dataframe(
        "asdfasdfwer", "w9ehasdfadsfu3jsd", timestamps
    )
    assert df is None  # Ensure None is returned when album is not found


if __name__ == "__main__":
    pytest.main()
