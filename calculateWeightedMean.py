from getData import get_album_tracks_dataframe

album_name = "Quantity Is Job 1 EP"
artist_name = "Five Iron Frenzy"

df = get_album_tracks_dataframe(album_name, artist_name)
# if df is not None:
#     print(df)

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

# Display weighted means
for feature, weighted_mean_value in weighted_means.items():
    print(f"Weighted Mean {feature.capitalize()}: {weighted_mean_value}")


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
