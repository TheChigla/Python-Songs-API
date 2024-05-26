import requests
import json
import sqlite3


# Get data from the API via the search endpoint and return it as a JSON object
querystring = {"q": input("Enter the name of the song: ")}


def get_data():
    headres = {
        "x-rapidapi-key": "d2c24fe424msha7774e191d09fe4p1ea858jsnff3af7d8490a",
        "x-rapidapi-host": "deezerdevs-deezer.p.rapidapi.com",
    }
    res = requests.get(
        "https://deezerdevs-deezer.p.rapidapi.com/search",
        headers=headres,
        params=querystring,
    )

    status_code = res.status_code
    got_headers = res.headers

    print(status_code, got_headers)

    return res.json()


data = {
    "title": get_data()["data"][0]["title"],
    "artist": get_data()["data"][0]["artist"]["name"],
    "album": get_data()["data"][0]["album"]["title"],
    "duration": get_data()["data"][0]["duration"],
    "preview": get_data()["data"][0]["preview"],
    "rank": get_data()["data"][0]["rank"],
}


def save_as_json():
    with open("song.json", "w") as file:
        json.dump(data, file, indent=2)


save_as_json()


# Save the data to a SQLite database
def save_to_db():
    conn = sqlite3.connect("songs.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        album TEXT,
        duration INTEGER,
        preview TEXT,
        rank INTEGER
    )"""
    )

    c.execute(
        """INSERT INTO songs (title, artist, album, duration, preview, rank)
    VALUES (:title, :artist, :album, :duration, :preview, :rank)""",
        data,
    )

    conn.commit()
    conn.close()


save_to_db()

print(data)
