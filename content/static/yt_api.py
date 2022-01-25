import json
import math
import isodate
import urllib

yt_api_key = "insert api key here"

def seconds_to_time(seconds_total):
    """Seconds to Time

    This method converts an amount of seconds into the corresponding amount of hours, minutes and seconds.

    :attr seconds_total: amount of seconds to be converted
    :type seconds_total: float

    :return: the amount of hours, minutes and seconds converted from seconds
    :rtype: tuple(int, int, int)
    """
    hour = math.floor(seconds_total/3600)
    minute = math.floor((seconds_total-3600*hour)/60)
    second = math.floor(seconds_total-3600*hour-60*minute)
    return hour, minute, second

def get_video_length(id):
    """Get Video Length

    Gets the length of a YouTube video in seconds from a YouTube id

    :attr id: the id of the YouTube video to get the length from
    :type id: str

    :return: the length of the video in seconds
    :rtype: float
    """
    yt_url = "https://www.googleapis.com/youtube/v3/videos?id="+id+"&key="+yt_api_key+"&part=contentDetails"
    response = urllib.request.urlopen(yt_url).read()
    data = json.loads(response)
    data_items=data['items']
    duration=data_items[0]['contentDetails']['duration']
    dur = isodate.parse_duration(duration)
    return dur.total_seconds()