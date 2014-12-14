import json
import urllib2
from hashlib import md5

from flask import request

from config import Config


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff <= 7:
        return str(day_diff) + " days ago"
    if day_diff <= 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff <= 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


def convert_to_type(original_value, data_type):
  if data_type == 'bool':
    converted_value = True if original_value=='1' else False
  elif setting.data_type == 'float':
    converted_value = float(original_value)
  else:
    converted_value = str(original_value)
  return converted_value

def convert_to_db_format(original_value, data_type):
  if data_type == 'bool':
    converted_value = '1' if original_value else '0'
  else:
    converted_value = str(original_value)
  return converted_value
