import zoneinfo
from datetime import datetime, timedelta
from urllib.request import urlopen

from .parser import NovaParser, Song


def get_playlist(url: str, local_tz: zoneinfo.ZoneInfo, offset: int) -> list[Song]:

    # The `data` kwarg is needed to force a POST request. Making a POST request
    # ensures that the CDN cache is bypassed and that the latest content is
    # retrieved.
    with urlopen(url, data=b"") as resp:
        data = resp.read().decode("utf-8")

    parser = NovaParser()
    parser.feed(data)
    songs = parser.songs
    for song in songs:
        song.time = localize(song.time, local_tz, offset)
    return songs


def localize(song_time: str, local_tz: zoneinfo.ZoneInfo, offset: int) -> str:
    hour, minute = song_time.split(":")

    paris_time = datetime.now(tz=zoneinfo.ZoneInfo("Europe/Paris"))
    paris_song_time = paris_time.replace(hour=int(hour), minute=int(minute))

    local_song_time = paris_song_time.astimezone(local_tz)
    display_time = local_song_time + timedelta(minutes=offset)

    return display_time.strftime("%H:%M")
