"""
Terrarium Package

The acquisition module contains functions required 
to find the latest acquisition image for a region.
"""
import ee
import datetime

def generate_image_identifier(image: ee.Image) -> str:
    """ 
    A function that returns the identifer for the given Earth Engine Image.
    The function assumes the Image is a Sentinel-2 L2A Image.
    """
    # Construct and return the image identifier
    return f"COPERNICUS/S2_SR/{image.id().getInfo()}"

def generate_latest_date(geometry: ee.Geometry) -> datetime.datetime:
    """
    A function that returns a datetime object that represents date of the latest 
    available Sentinel-2 L2A acquisition for the given Earth Engine Geometry.
    """
    from . import temporal

    # Generate daterange spanning a week prior to the current date
    today = datetime.datetime.utcnow()
    weekrange = temporal.generate_daterange(date=today, days=7)

    # Define an ImageCollection for Sentinel-2 MSI L2A
    collection = ee.ImageCollection("COPERNICUS/S2_SR")
    # Filter the ImageCollection for the given geometry and the weekrange
    collection = collection.filterBounds(geometry).filterDate(*weekrange)

    # Generate a datelist for the filtered collection
    datelist = temporal.generate_datelist(collection)
    # Return the latest date from the datelist
    return datelist[-1]

def generate_latest_image(date: datetime.datetime, geometry: ee.Geometry) -> ee.Image:
    """
    A function that returns an Earth Engine Image that represents the latest available
    Sentinel-2 L2A acquisition by for the given Earth Engine Geometry by accepting an 
    expected acquisiton date value and creating a buffer around that date.

    The buffered date range is used to filter Images which are then tested for geometry
    coverage to ensure that the Image fully cover the given Geometry.
    """
    from . import temporal
    from . import spatial

    # Generate a daterange spanning a 1 day before and after the given date
    daybuffer = temporal.generate_datebuffer(date=date, buffer=1)

    # Define an ImageCollection for Sentinel-2 MSI L2A
    collection = ee.ImageCollection("COPERNICUS/S2_SR")
    # Filter the ImageCollection for the given geometry and the daybuffer
    collection = collection.filterBounds(geometry).filterDate(*daybuffer)

    # Check if there are any acquisitions in the time period
    if collection.size().getInfo() == 0:
        return None

    # Filter the ImageCollection based on geometry coverage
    filtered_collection = spatial.filter_coverage(collection, geometry)

    # Return the first Image from the filtered ImageCollection
    return filtered_collection.first()
