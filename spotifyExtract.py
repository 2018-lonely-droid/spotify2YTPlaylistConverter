import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Create api
def connect(clientID, clientSecret):
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=clientID, client_secret=clientSecret
        )
    )
    return sp


# Fetch the playlist
def fetchPlaylistById(api, id):
    # Get first 100 songs on playlist
    response = api.playlist(playlist_id=id)
    playlistResponse = response['tracks']
    playlistItems = playlistResponse['items']

    # Get playlist name & create username
    playlistName = response['name']
    playlistUser = playlistItems[0]['added_by']['id']

    # Get playlist thumbnail URL
    img = api.playlist_cover_image(playlist_id=id)
    playlistThumbnail = img[0]['url']

    # Paginate through the rest if more songs
    while playlistResponse['next']:
        playlistResponse = api.next(playlistResponse)
        playlistItems.extend(playlistResponse['items'])
    return playlistUser, playlistName, playlistThumbnail, playlistItems


# Fetch playlist user info
def fetchPlaylistUser(api, user):
    response = api.user(user)
    return response


# Extract song data from playlist
def extractSongs(api, playlistItems):
    spotifyPlaylist = []
    for i in playlistItems:
        song = {}
        song['track_name'] = i['track']['name']
        song['artist_name'] = i['track']['artists'][0]['name']
        song['album_name'] = i['track']['album']['name']
        spotifyPlaylist.append(song)
    return spotifyPlaylist


# Build queries to search on Youtube
def query_builder(pl_data):
    queries = []
    for obj in pl_data:
        q = "{} {} {}".format(obj['track_name'], obj['album_name'], obj['artist_name'])
        queries.append(q)
    return queries




