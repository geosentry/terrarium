"""
Terrarium Package

The export module contains functions for exporting acquisition assets
"""
import ee

def export_image_asset(image: ee.Image, geometry: ee.Geometry, name: str) -> ee.batch.Task:
    """ 
    A function that creates an export task for the given Earth Engine Image.
    The image is exported to the 'terrascope-assets' bucket as a GeoTIFF with the given 
    name and cropped to the given Geometry at a 1m spatial resolution and a CRS of EPSG:4326.
    """
    # Define the export configuration
    exportconfig = {
        "bucket": "terrascope-assets",
        "scale": 1,
        "crs": "EPSG:4326",
        "maxPixels": 100000000,
        "fileFormat": "GeoTIFF",
        "skipEmptyTiles": True,
        "image": image,
        "description": f"export"[0:100],
        "fileNamePrefix": name,
        "region": geometry
    }

    # Create and returns the export configuration
    return ee.batch.Export.image.toCloudStorage(**exportconfig)
