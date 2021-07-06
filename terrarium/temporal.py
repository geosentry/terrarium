"""
Terrarium Package

The temporal package contains functions for temporal manipulations
"""
import ee
import typing
import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

def generate_date_timestamp(posixstamp: int) -> datetime.datetime:
    """ A function that returns a datetime object for a given POSIX timestamp. """
    return datetime.datetime.utcfromtimestamp(int(posixstamp/1000))

def generate_date_googledate(date: DatetimeWithNanoseconds) -> datetime.datetime:
    """ A function that returns a datetime object for a given DatetimeWithNanoseconds object. """
    return datetime.datetime.fromisoformat(date.isoformat()).replace(tzinfo=None)

def generate_googledate_date(date: datetime.datetime) -> DatetimeWithNanoseconds:
    """ A function that returns a DatetimeWithNanoseconds object for a given datetime object. """
    return DatetimeWithNanoseconds.fromisoformat(date.isoformat())

def generate_date_nextacquisition(date: datetime.datetime) -> datetime.datetime:
    """ A function that returns a datetime object for the next acquisition given another acquisition date. """
    # Sentinel-2 MSI Acquisitions occur every 5 days
    return date + datetime.timedelta(days=5)

def generate_daterange(date: datetime.datetime, days: int) -> typing.Tuple[datetime.datetime]:
    """ 
    A function that returns a datetime tuple with two dates for a given date and the number 
    of days in the range. The first date in the tuple represents the beginning of the range and 
    the second date represents the given date or the end of the range.
    """
    # Generate a datetime object for the width number of day before the given date
    begin = date - datetime.timedelta(days=days)
    # Return the tuple of dates
    return (begin, date)

def generate_datebuffer(date: datetime.datetime, buffer: int) -> typing.Tuple[datetime.datetime]:
    """
    A function that returns a datetime tuple with two dates for a given date and the number 
    of buffer days around it. The first date in the tuple represents the beginning of the range
    which is the buffer number of days before the given date and the second date represents the
    end of the range with buffer number of days after the given date.
    """
    # Generate a datetime object for the buffer number of days before the given date
    start = date - datetime.timedelta(days=buffer)
    # Generate a datetime object for the buffer number of days after the given date
    end = date + datetime.timedelta(days=buffer)
    # Return the tuple of dates
    return (start, end)

def generate_datelist(collection: ee.ImageCollection) -> typing.List[datetime.datetime]:
    """
    A function that returns a list of datetime object representing the unique dates in a 
    given Earth Engine ImageCollection. The returned datelist sorted chronologically.
    """
    # Aggregate the timestamps of every Image in the ImageCollection as a list of POSIX timestamps
    timestamps = collection.aggregate_array("system:time_start").getInfo()
    # Accumulate the timestamps into a list of datetime objects
    datelist = [generate_date_timestamp(posix_stamp) for posix_stamp in timestamps]
    # Sort the datetime objects in the list
    datelist.sort()
    # Return the datelist
    return datelist
