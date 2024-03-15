"""
Scrapes Pitchfork for album names, artist names, ratings, and genres
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import time

album_links = []
albums_artists = []
albums = {}


# From page 1 to 2194 for latest reviews
# 1 to 423 for electronic
# 1 to 213 for pop/r&b
# 1 to 998 for rock
# 1 to 64 for jazz
# 1 - 243 for rap
# for i in range(100, 2195):
genres = (
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

genre = genres[2]  # jazz
has_next_page = True
page_num = 1

# read df as csv and store as df
prev_df = pd.read_csv(f"data/{genre}_pitchfork.csv")

new_df = pd.DataFrame(
    columns=["artist", "album_name", "rating", "album_link", "genre"]
)

while has_next_page:
    url = f"https://pitchfork.com/reviews/albums/?genre={genre}&page={page_num}"
    # url = "https://pitchfork.com/reviews/albums/"
    page = requests.get(url)
    if page.status_code != requests.codes.ok:
        has_next_page = False
        continue

    time.sleep(0.5)
    soup = BeautifulSoup(page.text, "html.parser")

    for div in soup.find_all("div", class_="review"):

        try:  # if any aspect (artist, album name, rating, genre) is missing, we will skip over the album
            link = div.find("a", href=True)["href"]

            album_review = div.find("div", class_="review__title")
            artist = album_review.find("li").get_text()
            album_name = album_review.find("em").get_text()
            albums_artists.append((artist, album_name))  # tuple?

            album_link = "https://pitchfork.com" + str(link)
            album_page = requests.get(album_link)

            time.sleep(0.5)
            album_soup = BeautifulSoup(album_page.text, "html.parser")
            score = album_soup.find(class_=re.compile("Rating")).get_text()
            # albums[str(artist + "-:-" + album_name)] = score

            # check if review is a duplicate
            next_row = {
                "artist": [artist],
                "album_name": [album_name],
                "rating": [score],
                "album_link": [album_link],
                "genre": [genre],
            }

            if ~(
                (
                    (artist in prev_df.loc[:, "artist"])
                    & (album_name in prev_df.loc[:, "album_name"])
                    & (score in prev_df.loc[:, "rating"])
                    & (album_link in prev_df.loc[:, "album_link"])
                    & (genre in prev_df.loc[:, "genre"])
                )
            ):
                new_df = new_df._append(next_row, ignore_index=True)

        except AttributeError:
            continue

    page_num += 1


new_df = new_df._append(prev_df, ignore_index=True)
new_df.to_csv(f"data/{genre}_pitchfork.csv")
