import json
import math
import isodate
import urllib
from django.utils.translation import gettext_lazy as _

#import collab_coursebook.settings_secrets as secrets

yt_api_key = ""#secrets.YT_API_KEY

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

def seconds_to_timestamp(seconds):
    """Get Video Length

    Converts an amount of seconds into a timestamp of the format HH:MM:SS

    :attr seconds: the amount of seconds to be converted
    :type id: int

    :return: the converted timestamp
    :rtype: String
    """
    hour, minute, second = seconds_to_time(seconds)
    timestamp =  ""
    if (hour > 0):
        timestamp += f"{hour}:"
    if (hour > 0 and minute < 10):
        timestamp += "0"
    timestamp += f"{minute}:"
    if (second < 10):
        timestamp += "0"
    timestamp += f"{second}"

    return timestamp

def timestamp_to_times(timestamp):
    """Get Video Length

    Extracts hours, minutes and seconds from a timestamp of the format HH:MM:SS

    :attr timestamp: the timestamp to extract times from
    :type id: String

    :return: the extracted times from the timestamp
    :rtype: tuple(int, int, int)
    """
    times = timestamp.split(":")

    if len(times) == 3:
        hour = times[0]
        minute = times[1]
        second = times[2]
    else:
        hour = 0
        minute = times[0]
        second = times[1]

    return hour, minute, second

def timestamp_to_seconds(timestamp):
    """Get Video Length

    Converts a timestamp in the format HH:MM:SS to seconds

    :attr timestamp: the timestamp convert into seconds
    :type id: String

    :return: the amount of seconds in the timestamp
    :rtype: int
    """
    hour, minute, second = timestamp_to_times(timestamp)
    seconds = int(hour) * 3600 + int(minute) * 60 + int(second)
    return seconds

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

def time_to_string(total_hours, total_minutes, total_seconds):
    vid_len = ""
    if total_hours > 0:
        vid_len += f"{total_hours} " + _("Hours")
        if total_minutes or total_seconds > 0: 
            vid_len += ", "
    if total_minutes > 0:
        vid_len += f"{total_minutes} " + _("Minutes")
        if total_seconds > 0: 
            vid_len += ", "
    if (total_seconds > 0) or total_hours and total_minutes == 0:
        vid_len += f"{total_seconds} " + _("Seconds")
    return vid_len