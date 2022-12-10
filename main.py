import os
import re
import json
from spotifyExtract import connect, fetchPlaylistById, fetchPlaylistUser, extractSongs, query_builder
from ytmusicapi import YTMusic
from dotenv import load_dotenv
load_dotenv() # Load .env file
ytmusic = YTMusic('headers_auth.json') # Load authenticated cookie creds for youtube music


def main():
    # Get spotify playlist id from url
    playlistURL = input('Please enter your Spotify Playlist URL: ')
    playlistID  = re.search('.*\/(.*)\?', playlistURL).groups()[0]
    # Connect to spotify
    spotifyAPI = connect(os.environ.get('clientID'), os.environ.get('clientSecret'))
    print('Connected to Spotify')
    # Fetch playlist songs
    playlistUser, playlistName, playlistThumbnail, playlistItems = fetchPlaylistById(spotifyAPI, playlistID)
    queries = query_builder(extractSongs(spotifyAPI, playlistItems))
    # Fetch user URL & follower count
    playlistUserMetaData = fetchPlaylistUser(spotifyAPI, playlistUser)
    # Build description
    ytMusicDescription = (  'Made by: ' + str(playlistUserMetaData['display_name']) +  
                            ' | Followers: ' +  str(playlistUserMetaData['followers']['total']) +  
                            ' | Profile: ' +  'https://open.spotify.com/user/' + str(playlistUserMetaData['id']) +
                            ' | Thumbnail: ' + str(playlistThumbnail))
    print('Fetched Spotify playlist')

    # Loop through spotify songs
    videoIds = []
    for song in queries:
        # Search for matching song title and load top result video id
        match = ytmusic.search(query=song, filter='songs', limit=1)
        print(str(match[0]['title']) + ' | Album: ' + str(match[0]['album']['name']) + ' | Duration: ' + str(match[0]['duration']))
        videoIds.append(match[0]['videoId'])

    # Insert songs into YT playlist
    ytmusic.create_playlist(title=playlistName, description=ytMusicDescription, video_ids=videoIds)
    print("Finished migrating")


main()



