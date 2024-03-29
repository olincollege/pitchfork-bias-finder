# Pitchfork Bias Finder

## Overview
The Bias in Album Ratings project aims to investigate potential biases in album ratings by analyzing the influence of music features. By exploring the relationship between music characteristics and subjective evaluations, this project seeks to uncover underlying biases within the rating process and examine their implications for the perception of musical quality.

The computational essay is in the `pitchfork_bias_finder.ipynb` file

## Key Objectives
- Identify potential biases in album ratings based on music features.
- Explore the relationship between music characteristics and subjective evaluations.

## Usage & Dependencies

1. Clone the repository
    ```
    git clone https://github.com/olincollege/pitchfork-bias-finder.git 
    ```
    When cloning this repository, take note that the data we've collected from
    scraping pitchfork and spotify are in the following directories:
    `pitchfork_data/` and `data_final/`. 

2. Navigate to the project direcotry:
   ```
   cd pitchfork-bias-finder
   ```
3. Install the required dependencies

    The `requirements.txt` file contains the necessary dependencies to run the
    scrapers `get_pitchfork_data.py` and `get_spotify_data.py`, as well as the
    computational essay. To install these dependencies, please run the following
    command in a virtual environment:

    ```
    pip install -r requirements.txt
    ```
4. Create a file `config.py` in the root of the repository

    The `config.py` file must define these two variables:
    ```
    CLIENT_ID = "your client id"
    CLIENT_SECRET = "your client secret"
    ```
    With these variables, your API key is set up to access the Spotify API's
    diverse toolset that we implemented for this project.

5. Run the project:
   - to get pitchfork data: 
        ```
        python3 get_pitchfork_data.py
        ```
   - to get spotify album features: 
        ```
        python3 process_album_data.py
        ```
   - overview & analysis: 
    `pitchfork_bias_finder.ipynb`
   
## Contributing

The project was conducted by Sally Lee, Eddy Pan, and Vishnu Eskew.

Contributions to this project are welcome! If you have ideas for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License.
