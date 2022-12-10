import argparse
import sys
import zoneinfo

from .nova import NovaError, get_playlist


def main() -> None:
    args = parse_args()

    try:
        songs = get_playlist(args.url, args.timezone, args.offset)
    except NovaError as err:
        sys.stderr.write(f"nova: {err}\n")
        sys.exit(1)

    for song in songs:
        print(f"{song.time}  {song.artist} — {song.title}")


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
    parser.add_argument(
        "-u",
        "--url",
        default="https://www.nova.fr/radios/radio-nova/",
        type=str,
        help="URL where the playlist can be found",
    )
    return parser.parse_args()


def to_tz(tz_name: str) -> zoneinfo.ZoneInfo:
    if tz_name not in zoneinfo.available_timezones():
        raise argparse.ArgumentTypeError(f"{tz_name} is not a valid time zone")
    return zoneinfo.ZoneInfo(tz_name)
