from pathlib import Path

import pytest

from nova_playlist.parser import NovaParser, Song, has_class, is_complete_song

datadir = Path(__file__).parent / "testdata"


def test_parser():
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
                    <h2><a>JOHN FAHEY</a></h2>
                    <p>SUNFLOWER RIVER BLUES</p>
                </div>
                </div>

                <div class="wwtt_content">
                <p class="time">03:05</p>
                <div class="wwtt_right">
                    <div class="wwtt_imgcontent">
                    <a class="img_wwtt">
                        <img src="." />
                    </a>
                    </div>
                    <h2><a>ZELIA BARBOSA</a></h2>
                    <p>FUNERAL DO LAVRADOR</p>
                </div>
                </div>
            </body>
        </html>
    """

    parser = NovaParser()
    parser.feed(data)

    assert parser.songs == [
        Song(artist="John Fahey", title="Sunflower River Blues", time="03:07"),
        Song(artist="Zelia Barbosa", title="Funeral Do Lavrador", time="03:05"),
    ]


def test_parser_incomplete_data():
    # As above, but missing markup for title of first song
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
                    <h2><a>JOHN FAHEY</a></h2>
                </div>
                </div>

                <div class="wwtt_content">
                <p class="time">03:05</p>
                <div class="wwtt_right">
                    <div class="wwtt_imgcontent">
                    <a class="img_wwtt">
                        <img src="." />
                    </a>
                    </div>
                    <h2><a>ZELIA BARBOSA</a></h2>
                    <p>FUNERAL DO LAVRADOR</p>
                </div>
                </div>
            </body>
        </html>
    """
    parser = NovaParser()
    parser.feed(data)

    assert parser.songs == [
        Song(artist="Zelia Barbosa", title="Funeral Do Lavrador", time="03:05"),
    ]


def test_real_data():
    with open(datadir / "actual-full-page.html", encoding="utf-8") as f:
        data = f.read()

    parser = NovaParser()
    parser.feed(data)

    expected = [
        Song(artist="Fatback Band", title="Feel My Soul", time="03:13"),
        Song(artist="Shogun Orchestra", title="Jacmel", time="03:07"),
        Song(artist="Nepal", title="Sundance", time="03:04"),
        Song(artist="Laura Marling", title="Soothing", time="03:00"),
        Song(artist="Reginald Omas Mamode Iv", title="I Guess", time="02:56"),
        Song(artist="Christophe", title="I Sing For ...", time="02:53"),
        Song(artist="Alicia Keys", title="Feeling U Feeling Me", time="02:51"),
        Song(artist="Busta Rhymes", title="Everything Remains Raw", time="02:47"),
        Song(artist="Sarah Maison", title="La Nuit", time="02:44"),
        Song(artist="The Maytones", title="If Loving You Is Wrong", time="02:40"),
    ]
    assert parser.songs == expected


@pytest.mark.parametrize(
    ["name", "attrs", "expected"],
    [
        ("hello", [("class", "hello")], True),
        ("hello", [("class", "world")], False),
        ("hello", [("aria-label", "hello")], False),
    ],
)
def test_has_class(name, attrs, expected):
    assert has_class(name, attrs) == expected


@pytest.mark.parametrize(
    ["data", "expected"],
    [
        ({"artist": "hello", "title": "world", "time": "01:23"}, True),
        ({"artist": "hello", "time": "01:23"}, False),
        ({}, False),
        ({"artist": "hello", "title": "world", "time": ""}, False),
    ],
)
def test_is_complete_song(data, expected):
    assert is_complete_song(data) == expected
