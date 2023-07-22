import random
import zoneinfo
from urllib.error import URLError

import pytest

from nova_playlist.nova import NovaError, get_playlist, localize
from nova_playlist.parser import Song

# Only testing with Paris time zone to avoid non-deterministic failures due to
# Daylight Saving Time happening at different times in different time zones.
paris_tz = zoneinfo.ZoneInfo("Europe/Paris")


@pytest.mark.parametrize(
    ["time", "timezone", "offset", "expected"],
    [
        ("01:23", paris_tz, 0, "01:23"),
        ("01:23", paris_tz, 6, "01:29"),
        ("01:23", paris_tz, -16, "01:07"),
    ],
)
def test_localize(time, timezone, offset, expected):
    assert localize(time, timezone, offset) == expected


@pytest.mark.parametrize(
    ["timezone", "offset", "expected_time"],
    [
        (paris_tz, 0, "03:07"),
        (paris_tz, 6, "03:13"),
        (paris_tz, -6, "03:01"),
    ],
)
def test_get_playlist(timezone, offset, expected_time, httpserver):
    data = b"""
        <html>
            <body>
                <div class="wwtt_content">
                <p class="time">03:07</p>
                <div class="wwtt_right">
                    <div class="wwtt_imgcontent">
                    <a class="img_wwtt">
                        <img src="." />
                    </a>
                    </div>
                    <h2><a>BRIGITTE FONTAINE & ARESKI</a></h2>
                    <p>C'EST NORMAL</p>
                </div>
                </div>
            </body>
        </html>
    """
    httpserver.expect_request(uri="/", method="POST").respond_with_data(data)
    playlist_url = httpserver.url_for("/")

    songs = get_playlist(playlist_url, timezone, offset)

    assert songs == [
        Song(
            artist="brigitte fontaine & areski",
            title="c'est normal",
            time=expected_time,
        )
    ]


def test_get_playlist__invalid_url():
    playlist_url = "invalid-url"
    with pytest.raises(NovaError) as exc_info:
        get_playlist(playlist_url, paris_tz, 0)

    assert isinstance(exc_info.value.__cause__, ValueError)


def test_get_playlist__server_unavailable():
    # Hopefully nothing is listening on that random port
    port = random.randint(12345, 2**16 - 1)
    playlist_url = f"http://localhost:{port}"

    with pytest.raises(NovaError) as exc_info:
        get_playlist(playlist_url, paris_tz, 0)

    assert isinstance(exc_info.value.__cause__, URLError)


def test_get_playlist__error_response(httpserver):
    httpserver.expect_request(uri="/", method="POST").respond_with_data(
        "Something went wrong", status=500
    )
    playlist_url = httpserver.url_for("/")

    with pytest.raises(NovaError) as exc_info:
        get_playlist(playlist_url, paris_tz, 0)

    assert exc_info.match(playlist_url)
    assert exc_info.match("code 500")


def test_get_playlist__unicode_decode_error(httpserver):
    data = """
        <html>
            <body>
                <div class="wwtt_content">
                <p class="time">03:07</p>
                <div class="wwtt_right">
                    <div class="wwtt_imgcontent">
                    <a class="img_wwtt">
                        <img src="." />
                    </a>
                    </div>
                    <h2><a>BRIGITTE FONTAINE & ARESKI</a></h2>
                    <p>C'EST NORMAL</p>
                </div>
                </div>
            </body>
        </html>
    """.encode(
        "utf-16"
    )
    httpserver.expect_request(uri="/", method="POST").respond_with_data(data)
    playlist_url = httpserver.url_for("/")

    with pytest.raises(NovaError) as exc_info:
        get_playlist(playlist_url, paris_tz, 0)

    assert isinstance(exc_info.value.__cause__, UnicodeDecodeError)
