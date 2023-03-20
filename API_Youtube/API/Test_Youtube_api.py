import os
from .tasks import celery_fetch

# from .models import Videos
# from API_Youtube import settings
# from datetime import datetime, timedelta
# from time import sleep

# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# SYNC_INTERVAL = int(os.environ["SYNC_INTERVAL"] if "SYNC_INTERVAL" in os.environ else 10)

def getnewposts():
    celery_fetch.delay(0)

# def getnewposts():

#     apikeys = settings.API_KEYS                   
#     # current_time = datetime.now()                 
    
#     # req_time = current_time - timedelta(minutes=5)
    
#     # flag=False
#     print("Starting Sync Service!!\n")
#     # try:
#     while True:
#         for apikey in apikeys:
#             try:
#                 # Http("hereeeee")
                
#                 youtube = build("youtube", "v3", developerKey=apikey)

#                 videos = Videos.objects.all().order_by("-publishingDateTime")
#                 if videos.exists():
#                     published_time = videos.first().publishingDateTime.replace(tzinfo=None)
#                 else:
#                     published_time = datetime.now() - timedelta(minutes=30)
#                 # req_time = published_time.isoformat("T") + "Z"

#                 req = youtube.search().list(q="valorant",part="snippet", order="date",
#                                             maxResults=50, publishedAfter=(published_time.replace(microsecond=0).isoformat()+'Z') )
                
#                 response = req.execute()

#                 # flag=True
#                 num_videos_fetched = len(response['items'])
#                 if num_videos_fetched > 0:
#                     for obj in response['items']:
#                         title = obj['snippet']['title']
#                         description = obj['snippet']['description']
#                         publishingDateTime = obj['snippet']['publishedAt']
#                         thumbnailsUrls = obj['snippet']['thumbnails']['default']['url']
#                         channelTitle = obj['snippet']['channelTitle']

#                         Videos.objects.create(title=title, description=description,
#                                 publishingDateTime=publishingDateTime, thumbnailsUrls=thumbnailsUrls,
#                                 channelTitle=channelTitle)
#                 print("Sync Completed successfully at {}".format(datetime.utcnow()))

#             except HttpError as er:
#                 err_code = er.resp.status
#                 if not(err_code == 400 or err_code == 403):
#                     break
#             # except KeyboardInterrupt:
#             #     print("hereeeee")
#             #     break

#             finally:
#                 sleep(SYNC_INTERVAL)
#     # except KeyboardInterrupt:
#     #     print("here")
#     #     pass
    
#     # print("here")
