# Automate Spotify with Python

# Find out good music list and generate at Spotify
# Login into the Youtube 
'''
Step 1: Log into Youtube
Step 2: Grab our Liked Videos
Step 3: Create a new palylist
Step 4: Search for the song
Steop 5: Add this song into the new Spotify playlist
'''

import json
import requests
from secrets import spotifty_user_id
import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class CreatePlaylist:
    def __init__(self):
        self.user_id = spotifty_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    # Step 1: Log into Youtube
    def get_youtube_client(self):
        # copied from Youtube Data API
        # Disable OAuthlib's HTTPs verification when running locally.
        # *DO NOT* leave this option enabled when running in production.
  
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        api_service_name = "Youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes=['profile', 'email'])
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        
        # from the Youtube DATA PAI
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials = credentials)

        return youtube_client

        SCOPES = ['https://www.googleapis.com/auth/yt-analytics-monetary.readonly']
    
    # Step 2: Grab our Liked videos & Creating A Dictionary Of Important Song Information
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="",
            myRating="like"
        )
        respont = request.execute()

        # collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # user youtube_dl to collect the song name & artist name
            video =- youtube.dlYoutubeeDL({}).extract_info(youtube_url, download=False_)
            song_name = video["track"]
            artist = video["artist"]

            # save all important info
            self.all_song_info[video_title] = {
                "youtube_url":youtube_url,
                "song_name":song_name,
                "artist":artist,
                
                #add the uri, easy to get song to put into playlist
                "spotify_uri":self.get_spotify_uri(song_name,artist)

                
            }
    
    # Step 3: Create a new playlist https://developer.spotify.com/console/post-playlists/
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Youtube Liked videos"
            "description" : "All Liked Youtube Videos"
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body,
            headers = {
                "Content-Type":"application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = respon.json()

        # playlist id
        return reponse_json["id"]
    # Step 4: Search for the song
    def get_spotify_uri(self, song_name, artist):
        
        queryt = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify.token)
            }
        )
        response_json = response.json()
        songs = response_json["Tracks"]["items"]
        
        # Only use the firstsong
        uri = songs[0]["uri"]

        return uri

 
    # Step 5: Add this song into the new Spotify platylist
    def add_song_to_playlist(self):
        # populate our songs dictionary
        self.get_liked_videos()

        #collect all of uri
        uris = []
        for song, info in self.all_song_info.items():
            uri.append(info["spotify_uri"]

        # create a new playist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "httpys://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data = request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify.token)
            }
        )
        response_json = response.json()
        return response_json
            
        )
