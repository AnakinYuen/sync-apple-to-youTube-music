# Sync Apple to YouTube Music (SAY)

SAY is a Python program for synchronizing Apple Music playlist songs to YouTube Music playlist.

## Prerequisites

### Google Account

A Google account is required to access YouTube Music and edit playlist items. Create a Google account if you don't have one.

### Firestore Database

Firestore Database is used to cache YouTube Music search results.  Follow this [guide](https://firebase.google.com/docs/admin/setup?hl=en&authuser=0&_gl=1*co50ld*_ga*MjAyODE3Mzg4Ni4xNzA4MDkzMjE3*_ga_CW55HF8NVT*MTcwODA5MzIxNy4xLjEuMTcwODA5MzkwNC4yNC4wLjA.#set-up-project-and-service-account) to set up a Firebase project and service account.

## Setup

### 1. Create and activate a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install depenencies

```sh
pip install -r requirements.txt
```

### 3. Generate YouTube Music OAuth authentication

```sh
ytmusicapi oauth
```

### 4. Create Firestore Database collection

Create a new collection named `Songs` under the default database

## Usage

1. Define environment variables

    * `FIREBASE_CREDENTIALS_PATH`: path to the firebase service account credential

    * `YOUTUBE_CREDENTIALS_PATH`: path to the YouTube Music OAuth credential

    * `YT_MUSIC_LANGUAGE`: select the search language for YouTube Music. See the support language value [here](https://ytmusicapi.readthedocs.io/en/stable/faq.html#which-values-can-i-use-for-languages)

    * `APPLE_MUSIC_PLAYLIST_URL`: Apple Music playlist URL

    * `YT_MUSIC_PLAYLIST_ID`: YouTube Music playlist ID

    ```sh
    FIREBASE_CREDENTIALS_PATH="./credentails/firebaseServiceAccountKey.json"
    YOUTUBE_CREDENTIALS_PATH="./credentails/youtubeMusicoOAuth.json"
    YT_MUSIC_LANGUAGE="ja"
    APPLE_MUSIC_PLAYLIST_URL="https://music.apple.com/jp/playlist/j-pop-now/pl.dc16cb58902342cba9711cbcd9bf2840"
    YT_MUSIC_PLAYLIST_ID="PL12AbcDE3f4Gh56E7iJklmNOPqrs_tuv8"
    ```

2. Run the program

```sh
python3 main.py
```

## Docker

## Build docker image
```sh
export IMAGE_TAG="say"
docker build -t $IMAGE_TAG .
```

## Run the container

```sh
export IMAGE_TAG="say"
docker run \
  -e FIREBASE_CREDENTIALS_PATH="./credentails/firebaseServiceAccountKey.json" \
  -e YOUTUBE_CREDENTIALS_PATH="./credentails/youtubeMusicoOAuth.json" \
  -e APPLE_MUSIC_PLAYLIST_URL="https://music.apple.com/jp/playlist/j-pop-now/pl.dc16cb58902342cba9711cbcd9bf2840" \
  -e YT_MUSIC_PLAYLIST_ID="PL12AbcDE3f4Gh56E7iJklmNOPqrs_tuv8" \
  -e YT_MUSIC_LANGUAGE="ja" \
  -v ./credentails:/app/credentails $IMAGE_TAG
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
