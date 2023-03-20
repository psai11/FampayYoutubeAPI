from API_Youtube.celery import app
from .models import Videos
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from API_Youtube import settings
from googleapiclient.errors import HttpError


apikeys = settings.API_KEYS 

@app.task
def task_one():
    print(" task one called and worker is running good")
    return "success"

@app.task
def task_two(data, *args, **kwargs):
    print(f" task two called with the argument {data} and worker is running good")
    return "success"

@app.task
def celery_fetch(api_value):
    try:
        # Http("hereeeee")
        
        youtube = build("youtube", "v3", developerKey=apikeys[api_value])

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

    except HttpError as er:
        err_code = er.resp.status
        if err_code == 403:
            print("API Error")
            next_api_number = (api_value + 1) % apikeys.count()
            # current_api = api_keys[current_api_number].key
            if next_api_number ==  apikeys.count() - 1:
                print("All APIs Exhausted")
            else:
                celery_fetch(next_api_number)
        if not(err_code == 400 or err_code == 403):
            print(er)
            pass
