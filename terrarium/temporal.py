"""
Terrarium Package

The temporal package contains functions for temporal manipulations
"""
import ee
import typing
import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

""" A set of conversion functions between different temporal data structures """

def datetime_fromtimestamp(posixstamp: int) -> datetime.datetime:
    """ A function that returns a datetime object for a given POSIX timestamp. """
    return datetime.datetime.utcfromtimestamp(int(posixstamp/1000))

def datetime_fromgoogledate(date: DatetimeWithNanoseconds) -> datetime.datetime:
    """ A function that returns a datetime object for a given DatetimeWithNanoseconds object. """
    return datetime.datetime.fromisoformat(date.isoformat()).replace(tzinfo=None)

def googledate_fromdatetime(date: datetime.datetime) -> DatetimeWithNanoseconds:
    """ A function that returns a DatetimeWithNanoseconds object for a given datetime object. """
    return DatetimeWithNanoseconds.fromisoformat(date.isoformat())

def googledate_fromtimestamp(posixstamp: int) -> DatetimeWithNanoseconds:
    """ A function that returns a DatetimeWithNanoseconds object for a given POSIX timestamp. """
    return DatetimeWithNanoseconds.utcfromtimestamp(int(posixstamp/1000))


""" A set of manipulation functions for temporal entities """

def shift_date(date: datetime.datetime, shift: int) -> datetime.datetime:
    """ A function that returns a datetime object for the next acquisition given another acquisition date. """
    return date + datetime.timedelta(days=shift)

def generate_daterange(date: datetime.datetime, width: int, buffer: bool = False) -> typing.Tuple[datetime.datetime]:
    """ 
    A function that returns a datetime tuple with two dates that represent the beginning and end of a temporal daterange. 
    The start of the daterange is 'width' number of days before the given 'date'. The end of the daterange is given 'date'
    unless the 'buffer' argument is set to True, in which case the end is 'width' number of days ahead of the given 'date'.
    """
    try:
        # Generate the start of the daterange
        start = shift_date(date, -width)
        # Generate the end of the daterange
        end = shift_date(date, width) if buffer else date

        # Return the tuple of dates
        return (start, end)

    except Exception as e:
        raise RuntimeError(f"could not generate daterange. error: {e}")

def generate_earthenginecollection_datelist(collection: ee.ImageCollection) -> typing.List[datetime.datetime]:
    """
    A function that returns a list of datetime object representing the unique dates in a 
    given Earth Engine ImageCollection. The returned datelist is sorted chronologically.
    """
    if not isinstance(collection, ee.ImageCollection):
        raise RuntimeError("could not generate datelist. collection must be a ee.ImageCollection.")

    try:
        # Aggregate the timestamps of every Image in the ImageCollection as a list of POSIX timestamps
        timestamps = collection.aggregate_array("system:time_start").getInfo()
        # Accumulate the timestamps into a list of datetime objects
        datelist = [datetime_fromtimestamp(posix_stamp) for posix_stamp in timestamps]
        # Sort the datetime objects in the list
        datelist.sort()
        
    except Exception as e:
        raise RuntimeError(f"could not generate daterange. error: {e}")

    # Return the datelist
    return datelist
