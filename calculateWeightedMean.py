import pandas as pd
from getData import get_album_tracks_dataframe
import glob
import time
import pdb


def get_weighted_mean(album_name, artist_name):
    df = get_album_tracks_dataframe(album_name, artist_name)
    if df is None:
        return None

    weighted_means = {}
    total_duration = df["duration_ms"].sum()

    for column in df.columns:
        if (
            column != "id"
            and column != "track"
            and column != "album"
            and column != "first_artist"
            and column != "all_artists"
        ):
            weighted_sum = (df[column] * df["duration_ms"]).sum()
            weighted_means[column] = weighted_sum / total_duration

    # # Display weighted means
    # for feature, weighted_mean_value in weighted_means.items():
    #     print(f"Weighted Mean {feature.capitalize()}: {weighted_mean_value}")

    # Create a DataFrame for the weighted means
    weighted_means_df = pd.DataFrame(weighted_means, index=[0])
    weighted_means_df["album_name"] = album_name
    weighted_means_df["artist_name"] = artist_name

    # Rearrange columns to have album_name and artist_name at the beginning
    cols = weighted_means_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    weighted_means_df = weighted_means_df[cols]

    return weighted_means_df


# get_weighted_mean(album_name, artist_name)
# album_name = "A Charlie Brown Thanksgiving (50th Anniversary Edition)"
# artist_name = "Vince Guaraldi"

# genre = "electronic"
# weighted_means_df = get_weighted_mean(album_name, artist_name)
# weighted_means_df["genre"] = genre
# print(weighted_means_df)


def process_album_data(row):
    album_name = row["album_name"][2:-2]
    artist_name = row["artist"][
        2:-2
    ]  # Removing square brackets from artist name
    genre = row["genre"][2:-2]  # Removing square brackets from genre
    rating = float(row["rating"][2:-2])
    weighted_means_df = get_weighted_mean(album_name, artist_name)
    if weighted_means_df is not None:
        weighted_means_df["genre"] = genre
        weighted_means_df["rating"] = rating
        return weighted_means_df


"""
# Read the CSV file into a DataFrame
df = pd.read_csv("data/ele  time.sleep(0.2)ctronic_pitchfork.csv")

# Process each row of the DataFrame using list comprehension
result_dfs = [process_album_data(row) for _, row in df.iterrows()]

# Concatenate the DataFrames in the result list
result_df = pd.concat(filter(None, result_dfs), ignore_index=True)
"""


folder_path = "data/"

for file_path in glob.glob(folder_path + "*.csv"):
    genre = file_path[5:-14]

    df = pd.read_csv(file_path)
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

    for _, row in df.iterrows():
        try:
            result = process_album_data(
                row
            )  # Call the function with the current row
            if result is not None:
                result_dfs = result_dfs._append(
                    result, ignore_index=True
                )  # Append the result to the list if recognized by spotify
        except TypeError:
            pass
        time.sleep(0.2)

    # Process each row of the DataFrame using list comprehension
    # result_dfs = [process_album_data(row) for _, row in df.iterrows()]
    result_dfs.to_csv(f"{genre}_final.csv")
    breakpoint()

    # print(result_dfs)
    # Concatenate the DataFrames in the result list
    # result_df = pd.concat(filter(None, result_dfs), ignore_index=True)


#######################################################################################
# Calculate mean for every feature
# means = {}
# standard_deviation = {}
# for column in df.columns:
#     if (
#         column != "id"
#         and column != "track"
#         and column != "album"
#         and column != "first_artist"
#         and column != "all_artists"
#     ):
#         means[column] = df[column].mean()
#         standard_deviation[column] = df[column].std()

# # Display means
# for feature, mean_value in means.items():
#     print(f"Mean {feature.capitalize()}: {mean_value}")
# for feature, std in standard_deviation.items():
#     print(f"Standard_deviation {feature.capitalize()}: {std}")
# Calculate weighted mean for every feature
