"""
Terrarium Package

The spectral module contains functions for generating
various spectral manipulation on acquisition images.
"""
import ee
import datetime

from . import palette
from . import temporal

def truecolor_algorithm(image: ee.Image) -> ee.Image:
    """ 
    An algorithm that takes in an ee.Image and outputs an ee.Image. 
    Suitable for use with ee.ImageCollection.map(algorithm).

    The algorithm transforms the Image into an upsampled True Color Image
    and assumes the provided Image is from the Sentinel-2 MSI L2A Collection.
    
    The transformation process includes two steps - composition and upsampling.

    #### Composition
    The images are composed by isolating the true color RGB
    bands which are the 'TCI_R', 'TCI_G' and 'TCI_B' bands.

    #### Upsampling
    The images are upsampled using bicubic interpolation at a 
    1m spatial resolution and then reprojected to the EPSG:4326 CRS.
    """
    try:
        # Isolate the True Color band components of the Image
        tcbase = image.select('TCI_R', 'TCI_G', 'TCI_B')

    except ee.EEException as e:
        raise ee.EEException(f"true color composition failed. {e}")

    try:
        # Upsample the true color image with bicubic interpolation
        upsampled = tcbase.resample('bicubic')
        # Reproject the upsampled image to it's native CRS at a 1m scale.
        tc = upsampled.reproject(tcbase.projection(), scale=1)

    except ee.EEException as e:
        raise ee.EEException(f"true color upsampling failed. {e}")

    # Return the final true color image
    return tc

def ndvi_algorithm(image: ee.Image) -> ee.Image:
    """
    An algorithm that takes in an ee.Image and outputs an ee.Image. 
    Suitable for use with ee.ImageCollection.map(algorithm).

    The algorithm transforms the Image into a focalized NDVI Image
    and assumes the provided Image is from the Sentinel-2 MSI L2A Collection.

    NDVI - Normalized Difference Vegetation Index is spectral 
    index used for determing vegetation health.

    The transformation process includes three steps - composition, upsampling and focalization.

    #### Composition
    The images are composed by performing spectral bandmath on the image with 
    the equation (NIR-RED)/(NIR+RED) where NIR is the Near-Infrared Wavelength 
    (Band 8) and RED is the Red Wavelength (Band 4).

    #### Upsampling
    The images are upsampled with bicubic interpolation at a 1m spatial 
    resolution and then reprojected to the EPSG:4326 CRS.

    ### Focalization
    The images are focalized by scaling each pixel value by one order of magnitude
    and rounding them down to the nearest whole number. The resultant image is then
    passed through a morphological reducer that uses a square kernel.
    """
    try:
        # Isolate the NIR and RED band components and add them to a dictionary
        values = {"NIR": image.select('B8'), "RED": image.select('B4')}
        # Generate the NDVI image and rename the resultant band
        ndvibase = image.expression("(NIR-RED)/(NIR+RED)", values).rename('NDVI')
        
    except ee.EEException as e:
        raise ee.EEException(f"ndvi composition failed. {e}")

    try:
        # Upsample the NDVI image with bicubic interpolation
        upsampled = ndvibase.resample('bicubic')
        # Reproject the upsampled image to it's native CRS at a 1m scale.
        upsampled = upsampled.reproject(ndvibase.projection(), scale=1)
    
    except ee.EEException as e:
        raise ee.EEException(f"ndvi upsampling failed. {e}")

    try:
        # Scale each pixel value in the image by one order of magnitude
        ndvi = ee.Image(upsampled).toFloat().multiply(10).toInt().toFloat()
        # Focalize the image with a morpohological reducer
        ndvi = ndvi.focal_median(kernelType="square", radius=5)

    except ee.EEException as e:
        raise ee.EEException(f"ndvi focalization failed. {e}")

    # Return the final NDVI image
    return ndvi

def generate_spectral_image(date: datetime.datetime, geometry: ee.Geometry, index: str) -> ee.Image:
    """ 
    A function that generates a spectral Image given the date as a datetime object, geometry
    as an ee.Geometry and a valid spectral index as a string to generate.

    Images are generated from the Sentinel-2 MSI L2A Collection by filtering the collection
    with a buffer around the given date and mapping the spectral algorithm on each Image in 
    the filtered ImageCollection. The transformed collection is then mosaic-ed into a single Image, 
    visualized with corresponding palette and clipped to the given geometry before being returned.

    Valid values for the 'index' argument are:
    - 'TCI' - True Color Index
    - 'NDVI' - Normalized Difference Vegetation Index
    
    (other values will be supported in the future)

    Refer to the spectral generation algorithm for each Index for details on how they are generated.
    """
    # Assign null values for algo and vis
    algo = None
    vis = None

    # Check the value of the index and set 
    # the algorithm and palett accordingly
    if index == "NDVI":               
        algo = ndvi_algorithm
        vis = palette.NDVIFOCAL

    elif index == "TCI":
        algo = truecolor_algorithm
        vis = palette.S2TRUECOLOR

    else:
        # Raise an exception if the index is not valid
        raise RuntimeError(f"unsupported index: {index}")    

    try:   
        # Create a temporal buffer around the given date
        buffer = daterange = temporal.generate_daterange(date, 0.5, buffer=True)

        # Define the Sentinel-2 MSI L2A Collection
        s2collection = ee.ImageCollection("COPERNICUS/S2_SR")
        # Filter the collection for the geometry and the temporal buffer
        collection = s2collection.filterBounds(geometry).filterDate(*buffer)
    
    except RuntimeError as e:
        raise RuntimeError(f"could not create temporal buffer. {e}")
    except ee.EEException as e:
        raise RuntimeError(f"could not create filtered collection. {e}")

    try:
        # Transform the collection by mapping the algorithm over it
        transformed_collection = collection.map(algo)
        # Mosaic the transformed collection into a single image.
        mosiacimage = transformed_collection.mosaic()

        # Apply a visualisation palette to the image.
        visimage = mosiacimage.visualize(**vis) 
        # Clip the image to the geometry.
        image = visimage.clip(geometry)

    except ee.EEException as e:
        raise RuntimeError(f"could not create spectral image. {e}")

    try:
        # Retrieve the projection of the Sentinel-2 Image    
        projection = transformed_collection.first().projection()
        # Reproject the clipped image to its native CRS.
        image = image.reproject(projection)

    except ee.EEException as e:
        raise RuntimeError(f"could not reproject spectral image. {e}")

    # Return the image
    return image
