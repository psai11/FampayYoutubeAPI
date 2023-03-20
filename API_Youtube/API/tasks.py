from __future__ import absolute_import, unicode_literals
from celery import shared_task

from API_Youtube.celery import app
from .models import Videos
from googleapiclient import discovery
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from API_Youtube import settings
# from googleapiclient.errors import HttpError
import urllib.error

apikeys = settings.API_KEYS 
# discovery.build(api, version, http=http, cache_discovery=False)
# @shared_task(name = "print_msg_with_name")
# def print_message(name, *args, **kwargs):
#   print("Celery is working!! {} have implemented it correctly.".format(name))

# @shared_task(name = "add_2_numbers")
# def add(x, y):
#   print("Add function has been called!! with params {}, {}".format(x, y))
#   return x+y

@shared_task(name = "fetch-videos")
def fetchYoutubeVids(api_value, *args, **kwargs):
    try:
        # Http("hereeeee")
        
        youtube = discovery.build("youtube", "v3", developerKey=apikeys[api_value], cache_discovery= False)

        videos = Videos.objects.all().order_by("-publishingDateTime")
        if videos.exists():
            published_time = videos.first().publishingDateTime.replace(tzinfo=None)
        else:
            published_time = datetime.now() - timedelta(minutes=30)
        # req_time = published_time.isoformat("T") + "Z"

        req = youtube.search().list(q="valorant",part="snippet", order="date",
                                    maxResults=50, publishedAfter=(published_time.replace(microsecond=0).isoformat()+'Z') )
        
        response = req.execute()

        # flag=True
        num_videos_fetched = len(response['items'])
        if num_videos_fetched > 0:
            for obj in response['items']:
                title = obj['snippet']['title']
                description = obj['snippet']['description']
                publishingDateTime = obj['snippet']['publishedAt']
                thumbnailsUrls = obj['snippet']['thumbnails']['default']['url']
                channelTitle = obj['snippet']['channelTitle']

                Videos.objects.create(title=title, description=description,
                        publishingDateTime=publishingDateTime, thumbnailsUrls=thumbnailsUrls,
                        channelTitle=channelTitle)
        print("Sync Completed successfully at {}".format(datetime.utcnow()))

    except urllib.error.HttpError as er:
        err_code = er.code
        if err_code == 403:
            print("API Error")
            next_api_number = (api_value + 1) % apikeys.count()
            # current_api = api_keys[current_api_number].key
            if next_api_number ==  apikeys.count() - 1:
                print("All APIs Exhausted")
            else:
                fetchYoutubeVids(next_api_number)
        if not(err_code == 400 or err_code == 403):
            print("Error here:",er.reason)
            pass
