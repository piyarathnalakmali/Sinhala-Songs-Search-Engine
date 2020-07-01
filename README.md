# Sinhala-Songs-Search-Engine

## Getting Started:
To start the search engine follow the instructions given below.

1. Download or clone the repository
2. Run an elasticsearch instance on port 9200
3. Index the dataset by running index_data.py script
4. Run the command flask run
5. Go to http://localhost:5000 to experience

## Data
The dataset for the project was scraped from the website [Sinhala Song Book](https://sinhalasongbook.com/). The search engine contains a collection of 817 songs. Each song in the preprocessed data set has 7 metadata fields except lyrics.
- Title
- list of artists
- list of writers
- list of composers (as music)
- number of views
- beat 
- list of genres. 

## Supported query types
* Search a song by any field
  - title - කුරුටු ගෑ ගී
  - artist name - නන්දා මාලනී ගැයූ ගීත
  - beat - 6/8 සින්දු
  - genre - වත්මන් ගීත
* Range queries - හොඳම සින්දු 10
* Synnonyms - මව් ගුණ ගීත
* Misspelled queries - කරුනරත දිවුල්ගනේ ගැයූ ගීත
