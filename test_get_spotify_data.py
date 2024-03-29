"""
Pytest for get_spotify_data.py
"""

import time
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
    # Test case: ensure timestamps more than thirty seconds ago get removed.
    timestamps = [
        time.time() - 40,
        time.time() - 35,
        time.time() - 20,
        time.time() - 15,
        time.time() - 10,
    ]
    timestamps_updated = check_rate_limit(timestamps)
    assert (
        len(timestamps_updated) == 4
    )  # Assert that the result array only contains timestamps that occurred
    # in the last thirty seconds (and the current time).

    # Test case: ensure timestamps array is sorted after adding new entry as a
    # result of function call.
    timestamps = [
        time.time() - 40,
        time.time() - 30,
        time.time() - 20,
        time.time() - 10,
    ]
    timestamps_updated = check_rate_limit(timestamps)
    print(sorted(timestamps_updated))
    assert (
        sorted(timestamps_updated) == timestamps_updated
    )  # Assert that the timestamps list that is returned by check_rate_limit
    # is sorted.


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
    album_tracks_df = get_album_tracks_dataframe(
        "Electricity", "Ibibio Sound Machine", timestamps
    )
    assert isinstance(
        album_tracks_df, pd.DataFrame
    )  # Ensure DataFrame is returned

    # Test case: album not found
    timestamps = []
    album_tracks_df = get_album_tracks_dataframe(
        "asdfasdfwer", "w9ehasdfadsfu3jsd", timestamps
    )
    assert (
        album_tracks_df is None
    )  # Ensure None is returned when album is not found


if __name__ == "__main__":
    pytest.main()
