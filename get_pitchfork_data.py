"""
Scrapes Pitchfork for album names, artist names, ratings, and genres
"""

import time
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
from scraper_functions import find_features_in_review

GENRES = (
    "electronic",
    "folk",  # and Country
    "jazz",
    "pop",  # and R&B
    "rock",
    "experimental",
    "global",
    "metal",
    "rap",  # and Hip-Hop
)  # from pitchfork.com


def main():
    """
    When called, scrapes Pitchfork for album names, artist names, ratings, and
    genres
    """
    has_next_page = True
    page_num = 1

    for genre in GENRES:
        # read df as csv and store as df
        try:
            with open(
                f"pitchfork_data/{genre}_pitchfork.csv", "x", encoding="utf-8"
            ) as file:
                file.write(",artist,album_name,rating,album_link,genre")

        except FileExistsError:
            pass
        data_df = pd.read_csv(f"pitchfork_data/{genre}_pitchfork.csv")

        while has_next_page:
            url = (
                f"https://pitchfork.com/reviews/albums/"
                f"?genre={genre}&page={page_num}"
            )
            page = rq.get(url, timeout=10)
            if page.status_code != rq.codes.ok:  # pylint: disable=no-member
                has_next_page = False
                continue

            time.sleep(0.5)
            soup = BeautifulSoup(page.text, "html.parser")

            for div in soup.find_all("div", class_="review"):
                data_df = find_features_in_review(div, genre, data_df)

            page_num += 1

        data_df.to_csv(f"pitchfork_data/{genre}_pitchfork.csv")


if __name__ == "__main__":
    main()
