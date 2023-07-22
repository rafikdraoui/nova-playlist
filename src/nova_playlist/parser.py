from dataclasses import dataclass
from html.parser import HTMLParser

TagAttr = tuple[str, str | None]


@dataclass
class Song:
    artist: str
    title: str
    time: str


class NovaParser(HTMLParser):
    """Extract information about recently played songs from Radio Nova's
    website.

    Here's an example of the expected markup for a single song:

        <div class="wwtt_content">
            <p class="time">03:07</p>
            <div class="wwtt_right">
                <div class="wwtt_imgcontent">
                    <a class="img_wwtt">
                        <img ... />
                    </a>
                </div>
                <h2><a>JOHN FAHEY</a></h2>
                <p>SUNFLOWER RIVER BLUES</p>
            </div>
        </div>
    """

    def __init__(self) -> None:
        super().__init__()

        # This will contain the list of songs found in the document
        self.songs: list[Song] = []

        # This will hold the data about the song currently being parsed
        self.current_song: dict[str, str] = {}

        # Indicates whether parser is currently within the markup for
        # a song/artist/title
        self.in_song = False
        self.in_artist = False
        self.in_title = False

        # Indicates whether the next piece of text should be recorded as being
        # the song artist/title/time
        self.record_artist = False
        self.record_title = False
        self.record_time = False

    def handle_starttag(self, tag: str, attrs: list[TagAttr]) -> None:
        if tag == "div" and has_class("wwtt_content", attrs):
            # Start of a new song
            self.in_song = True
            if is_complete_song(self.current_song):
                self.songs.append(Song(**self.current_song))
            self.current_song = {}

            # Reset parsing attributes in case the markup for the previous song
            # was incomplete
            self.in_artist = False
            self.in_title = False
            self.record_artist = False
            self.record_title = False
            self.record_time = False

        elif tag == "h2" and self.in_song and not self.in_artist:
            # Start of artist markup
            self.in_artist = True
        elif tag == "a" and self.in_artist:
            # Artist name is in the <a> tag text
            self.record_artist = True
        elif tag == "div" and has_class("wwtt_right", attrs):
            # Start of title markup
            self.in_title = True
        elif tag == "p" and self.in_title:
            # Song title is in the <p> tag text
            self.record_title = True
        elif tag == "p" and has_class("time", attrs):
            # Song time is in the <p> tag text
            self.record_time = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "html" and is_complete_song(self.current_song):
            # End of document. Make sure to save last song.
            self.songs.append(Song(**self.current_song))

    def handle_data(self, data: str) -> None:
        if self.record_artist:
            self.current_song["artist"] = data.lower()
            self.in_artist = False
            self.record_artist = False
        elif self.record_title:
            self.current_song["title"] = data.lower()
            self.in_title = False
            self.record_title = False
            self.in_song = False
        elif self.record_time:
            self.current_song["time"] = data
            self.record_time = False


def has_class(name: str, attrs: list[TagAttr]) -> bool:
    return name in (v for k, v in attrs if k == "class")


def is_complete_song(raw_song: dict[str, str]) -> bool:
    return all(raw_song.get(attr) for attr in ("artist", "title", "time"))
