"""
Terrarium Package

The export module contains functions for exporting acquisition assets
"""
import ee

def export_image(image: ee.Image, bucket: str, name: str) -> ee.batch.Task:
    """ 
    A function that creates an export task for the given Earth Engine Image.
    The image is exported to the 'terrascope-assets' bucket as a GeoTIFF with the given 
    name and cropped to the given Geometry at a 1m spatial resolution and a CRS of EPSG:4326.
    """
    # Define the export configuration
    exportconfig = {
        # Export Image
        "image": image,

        # Export Tranforms and Bounds
        "scale": 1,
        "region": image.geometry(),
        "crs": image.projection().crs(),
        
        # Destination Filename and Bucket
        "bucket": bucket,
        "fileNamePrefix": name,

        # Export Description
        "description": f"export"[0:100],
        
        # Export Constraints
        "maxPixels": 1e10,
        "skipEmptyTiles": True,
        "fileFormat": "GeoTIFF"
    }

    try:
        # Create an export task with the export configuration
        task = ee.batch.Export.image.toCloudStorage(**exportconfig)
        # Return the task
        return task

    except Exception as e:
        raise RuntimeError(f"could not create image export task. {e}.")

def get_taskstatus(operationid: str = None, taskid: str = None, project: str = None) -> dict:
    """
    A function that returns the status of an Earh Engine export task.
    Accepts the full operation ID string in the format of 'projects/{projectid}/operations/{taskid}' or
    accepts the taskid and project ID as arguments and constructs tje operation ID from them.

    The task ID for a Task object can be retrieved from its 'id' property.
    The operation ID for a Task object can be retrieved from its 'name' property.
    """
    # Check if operation ID is given
    if not operationid:
        # Check if task ID and project ID are given
        if not taskid or not project:
            raise RuntimeError("could not check task status. task ID and project ID must be specified if operation ID is not.")

        # Construct the operations identifier from the project ID and task ID
        operationid = f"projects/{project}/operations/{taskid}"

    try:
        # Retrieve the task status from Earth Engine
        status = ee.data.getOperation(operationid)
        # Return the task status
        return status

    except Exception as e:
        raise RuntimeError(f"could not check task status. {e}.")
