# nova-playlist

[Radio Nova][] plays amazing music at night.

There could be Fela Kuti, then hip-hop from the 1990s, then Motown, then Tuareg music, then some minimal electro, then Hungarian folk songs, then David Bowie, then Amazonian cumbia, then a French song that was released last month, then Sufi devotional music from Punjab, then Nina Simone, then a tune from the north-east of Brazil.
It's wild.

And if you, like me, live a few time zones west of Paris, you get to conveniently enjoy it all in the evening instead of having to be up in the middle of the night!

Often, I want to know which song is currently playing, so that I can find out more about it and the artist.
There is a [page][song-history] where one can find what music has aired on the Radio in the past, but it's buggy and a bit annoying to use.
And even if the page was great to use, it wouldn't be as great as using the command line for it!
_Ergo_ this little program.

## Installation

The package is available on the Python Package Index (PyPI) as [nova-playlist][].
The recommended way of installing it is with [pipx][].

Python 3.9 or above is required, along with a IANA timezone database on your system.
Unix-y systems should alreay have it, otherwise you can try installing `tzdata` from PyPI.

## Usage

    $ nova
    20:36  Orchestra Baobab - Liiti Liiti
    20:30  Chico Buarque - Construção
    20:27  Abner Jay - My Middle Name Is The Blues
    20:23  Brigitte Fontaine - Le Goudron
    ...

By default, the times are in the "Canada/Atlantic" time zone.
If you want them in another time zone, you can pass the `-t`/`--timezone` argument:

    $ nova -t Europe/Berlin
    03:12  Los Camperos De Valles - El Gallo
    03:09  Karen Dalton - Something On Your Mind
    03:04  Têtes Raides & Yann Tiersen - Ginette
    02:59  The Toraia Orchestra Of Algiers - Nar Houbi Techaal
    ...

## Caveat

This can be somewhat brittle.
Sometimes, the data stops being updated on the site.
Or the data gets updated, but the timestamps are 11 minutes off from what's playing in the stream.
Finally, if Radio Nova changes their HTML structure in any way, this could start failing miserably.
But so far, so good!

[Radio Nova]: https://www.nova.fr/radios/nova-la-nuit/
[nova-playlist]: https://pypi.org/project/nova-playlist/
[pipx]: https://pypa.github.io/pipx/
[song-history]: https://www.nova.fr/radios/radio-nova/
