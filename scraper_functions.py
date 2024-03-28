"""
Helper functions for scraping pitchfork.com's album reviews
"""

import re
import time
from bs4 import BeautifulSoup
import requests


def get_pitchfork_rating(album_pitchfork_link):
    """
    Finds pitchfork rating of an album given the link to the album's page on
    pitchfork.

    Args:
        album_pitchfork_link: A string representing the link to the album's
            pitchfork page

    Returns:
        A string representing the rating pitchfork reviewers gave the album.
        Returns None if the link does not have a rating.
    """
    album_page = requests.get(album_pitchfork_link)

    time.sleep(0.5)
    album_soup = BeautifulSoup(album_page.text, "html.parser")
    try:
        rating = album_soup.find(class_=re.compile("Rating")).get_text()
        return rating
    except AttributeError:
        return None


def find_features_in_review(div, genre, pitchfork_df):
    """
    Finds the features of each review div from pitchfork.com, including the
    artist name, album name, rating, album link on pitchfork, and genre.

    Args:
        div: A Tag object representing the div of each review on pitchfork.com
            containing an album's information
        genre: A string representing the genre of the album
        pitchfork_df: The pandas DataFrame object that has the following
            columns: "artist", "album_name", "rating", "album_link", and
            "genre". It doesn't matter if it has rows of data already populated
            in it or not. This DataFrame object will have the album review data
            from pitchfork.com appended to it.

    Returns:
        A pandas DataFrame object with columns "artist", "album_name",
        "rating", "album_link", and "genre". It has the data collected from
        the album review on pitchfork.com appended to the pre-existing data.
        Returns the same DataFrame object as the argument "df" if the div
        contains missing data.
    """

    # if artist, album name, rating, or genre is missing, we pass the album
    try:
        link = div.find("a", href=True)["href"]

        album_review = div.find("div", class_="review__title")
        artist = album_review.find("li").get_text()
        album_name = album_review.find("em").get_text()

        album_link = "https://pitchfork.com" + str(link)
        rating = get_pitchfork_rating(album_link)

        next_row = {
            "artist": [artist],
            "album_name": [album_name],
            "rating": [rating],
            "album_link": [album_link],
            "genre": [genre],
        }

        pitchfork_df = pitchfork_df._append(
            next_row, ignore_index=True
        )  # pylint: disable=protected-access

    except AttributeError:
        pass
    return pitchfork_df
