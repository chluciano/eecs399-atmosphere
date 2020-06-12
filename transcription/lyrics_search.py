import requests
import xmltodict


# this function gets song lyrics with based on lyrics matching the given words.
# played around with this for a while. now the idea is: pass in good keywords, get the lyrics, do sentiment analysis.
# based of the analyses, can get better matches.
# see get_song_lyrics below
def get_related_lyrics(lyricsIn):
    params = {
        ('lyricText', lyricsIn)
    }
    endpoint = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricText"
    response = xmltodict.parse(requests.get(
        endpoint,
        params=params
    ).text)
    print(response)

# see get song_related_lyrics above.
# alternatively, can also get song suggestions from spotify and pass them in and get the lyrics and analyze those.
# that is what this function is for
def get_song_lyrics(artistIn, songIn):
    params = {
        ('artist', artistIn),
        ('song', songIn)
    }
    endpoint = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"
    response = xmltodict.parse(requests.get(
        endpoint,
        params=params
    ).text)
    print(response)