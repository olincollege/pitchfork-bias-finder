"""
Test scraper functions to find and scrape data from pitchfork.com
"""

import pytest  # pylint: disable=unused-import
import requests
import pandas as pd
from bs4 import BeautifulSoup
from scraper_functions import get_pitchfork_rating, find_features_in_review


def test_get_pitchfork_rating():
    """
    Ensures that get_pitchfork_rating() in scraper_functions.py works as
    intended. Contains tests for a valid test case, invalid pitchfork link,
    valid link not pitchfork, and invalid link
    """

    # Test case: a working pitchfork.com album review link
    rating = get_pitchfork_rating(
        "https://pitchfork.com/reviews/albums/bleachers-bleachers/"
    )
    assert rating == "6.4"

    # Test case: valid link, incorrect pitchfork album review link
    rating = get_pitchfork_rating(
        "https://pitchfork.com/reviews/albums/link-that-does-not-exist/"
    )
    assert rating is None

    # Test case: valid link, but not a pitchfork link
    rating = get_pitchfork_rating("https://wikipedia.org")
    assert rating is None

    # Test case: invalid link, not a pitchfork link
    try:
        rating = get_pitchfork_rating("not a link")
        assert False
    except requests.exceptions.MissingSchema:
        assert True


def test_find_features_in_review():
    """
    Ensures that find_features_in_review() in scraper_functions works as
    intended. Contains tests for valid and invalid genres as well as empty
    dataframes and pre-populated dataframes.
    """

    # Check that the function correctly appends another row of album data
    # given a valid page of albums' divs, genre, and empty pitchfork_df.
    genre = "electronic"
    pitchfork_df = pd.DataFrame(
        {
            "artist": [],
            "album_name": [],
            "rating": [],
            "album_link": [],
            "genre": [],
        }
    )
    page = requests.get(
        f"https://pitchfork.com/reviews/albums/?genre={genre}&page=11",
        timeout=10,
    )
    soup = BeautifulSoup(page.text, "html.parser")
    divs = soup.find_all("div", class_="review")
    for div in divs:
        pitchfork_df = find_features_in_review(div, genre, pitchfork_df)
    # can't actually test for hard-coded album data because the albums on a
    # page change over time
    assert len(pitchfork_df) == 12

    # Check that the function does not append anything given an invalid genre.
    genre = "not a real genre!!!"
    pitchfork_df = pd.DataFrame(
        {
            "artist": [],
            "album_name": [],
            "rating": [],
            "album_link": [],
            "genre": [],
        }
    )
    page = requests.get(
        f"https://pitchfork.com/reviews/albums/?genre={genre}&page=1",
        timeout=10,
    )
    soup = BeautifulSoup(page.text, "html.parser")
    divs = soup.find_all("div", class_="review")
    for div in divs:
        pitchfork_df = find_features_in_review(div, genre, pitchfork_df)
    assert len(divs) == 0
    assert len(pitchfork_df) == 0

    # Check that the function can append on top of a DataFrame that already has
    # data in it. Also check that the function works on different valid genres.
    genre = "jazz"
    pitchfork_df = pd.DataFrame(
        {
            "artist": ["artist 1", "artist 2"],
            "album_name": ["album 1", "album 2"],
            "rating": ["7.8", "9.1"],
            "album_link": ["link 1", "link 2"],
            "genre": ["jazz", "jazz"],
        }
    )
    page = requests.get(
        f"https://pitchfork.com/reviews/albums/?genre={genre}&page=11",
        timeout=10,
    )
    soup = BeautifulSoup(page.text, "html.parser")
    divs = soup.find_all("div", class_="review")
    for div in divs:
        pitchfork_df = find_features_in_review(div, genre, pitchfork_df)
    assert len(pitchfork_df) == 14

    # Check that, with a pre-populated DataFrame object, the function does not
    # append anything given a parameter that is not a Tag object for div.
    try:
        genre = "not a real genre!!!"
        pitchfork_df = pd.DataFrame(
            {
                "artist": ["artist 1", "artist 2"],
                "album_name": ["album 1", "album 2"],
                "rating": ["7.8", "9.1"],
                "album_link": ["link 1", "link 2"],
                "genre": ["jazz", "jazz"],
            }
        )
        div = "This is a string, not a div"
        pitchfork_df = find_features_in_review(div, genre, pitchfork_df)
        assert False
    except TypeError:
        assert len(pitchfork_df) == 2
        assert True
