import argparse
import zoneinfo
from datetime import datetime, timedelta
from urllib.request import urlopen
from typing import Any

from bs4 import BeautifulSoup

Song = dict[str, str]
Element = Any  # dummy type for BeautifulSoup's HTML element

playlist_url = "https://www.nova.fr/radios/radio-nova/"
paris_time = datetime.now(tz=zoneinfo.ZoneInfo("Europe/Paris"))


def main() -> None:
    args = parse_args()
    playlist = get_playlist()
    for song in playlist:
        song["time"] = localize(args.timezone, song["time"], args.offset)
        print("{time}  {artist} - {title}".format(**song))


def to_tz(tz_name: str) -> zoneinfo.ZoneInfo:
    if tz_name not in zoneinfo.available_timezones():
        raise argparse.ArgumentTypeError(f"{tz_name} is not a valid time zone")
    return zoneinfo.ZoneInfo(tz_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Display information about the songs that recently played on Radio Nova",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--timezone",
        default="Canada/Atlantic",
        type=to_tz,
        help="Local time zone to display the song times in",
    )
    parser.add_argument(
        "-o",
        "--offset",
        default=0,
        type=int,
        help="Number of minutes that song times need to be shifted by",
    )
    return parser.parse_args()


def get_playlist() -> list[Song]:

    # The `data` kwarg is needed to force a POST request. Sending an empty body
    # will retrieve the latest information, i.e no need to provide `day`,
    # `month`, `hour`, etc. in the form data.
    resp = urlopen(playlist_url, data=b"")
    html = BeautifulSoup(resp.read(), "html.parser")
    items: list[Element] = html.find_all("div", class_="wwtt_content")
    return [parse_song(item) for item in items]


def parse_song(item: Element) -> Song:
    artist = item.find("h2").find("a").text.title()
    title = item.find("div", class_="wwtt_right").find("p").text.title()
    time = item.find("p", class_="time").text

    return {"artist": artist, "title": title, "time": time}


def localize(local_tz: zoneinfo.ZoneInfo, time: str, offset: int = 0) -> str:
    hour, minute = time.split(":")
    paris_song_time = paris_time.replace(hour=int(hour), minute=int(minute))
    local_song_time = paris_song_time.astimezone(local_tz)
    display_time = local_song_time + timedelta(minutes=offset)
    return display_time.strftime("%H:%M")
