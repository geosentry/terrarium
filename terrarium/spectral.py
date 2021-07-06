"""
Terrarium Package

The spectral module contains functions for generating
various spectral manipulation on acquisition images.
"""
import ee
from . import pallete

def generate_TrueColor(image: ee.Image) -> ee.Image:
    """ 
    A function that generates a visualized True Color Image for the given Earth Engine Image.
    The function assumes that the Image is from the Sentinel-2 MSI collection.

    The process of generating a True Color Image in this function includes 
    three steps - composition, upsampling and visualization.

    #### Composition
    True Color images are composed by isolating the true color RGB 
    bands which are the TCI_R, TCI_G and TCI_B bands.

    #### Upsampling
    True Color images are upsampled with bicubic interpolation at a 
    1m spatial resolution and then reprojected to the EPSG:4326 CRS.

    ### Visualization
    True Color images are visualized using a pre-defined 
    color pallete from the geocore.palette library.
    """
    try:
        # Isolate the True Color band components of the Image
        tcbase = image.select('TCI_R', 'TCI_G', 'TCI_B')

    except ee.EEException as e:
        raise RuntimeError(f"true color composition failed. {e}")

    try:
        # Upsample the true color image with bicubic interpolation
        upsampled = tcbase.resample('bicubic')
        # Reproject the upsampled image to the EPSG:4326 CRS
        upsampled = upsampled.reproject(crs="EPSG:4326", scale=1)

    except ee.EEException as e:
        raise RuntimeError(f"true color upsampling failed. {e}")

    try:
        # Apply the visualization pallete on the image
        visualized = upsampled.visualize(**pallete.S2TC)
    
    except ee.EEException as e:
        raise RuntimeError(f"true color visualization failed. {e}")

    # Return the final true color image
    return visualized


def generate_NDVI(image: ee.Image) -> ee.Image:
    """ 
    A function that generates a visualized NDVI Image for the given Earth Engine Image. 
    The function assumes that the Image is from the Sentinel-2 MSI collection.

    NDVI - Normalized Difference Vegetation Index.
    It is spectral index used for determing vegetation health. The process 
    of generating an NDVI Image in this function includes four steps -
    composition, upsampling, focalization and visualization

    #### Composition
    NDVI images are composed by performing spectral bandmath on the image with 
    the equation (NIR-RED)/(NIR+RED) where NIR is the Near-Infrared Wavelength 
    (Band 8) and RED is the Red Wavelength (Band 4).

    #### Upsampling
    NDVI images are upsampled with bicubic interpolation at a 1m spatial 
    resolution and then reprojected to the EPSG:4326 CRS.

    ### Focalization
    NDVI images are focalized by scaling each pixel value by one order of magnitude
    and rounding them down to the nearest whole number. The resultant image is then
    passed through a morphological reducer that uses a square kernel.

    ### Visualization
    NDVI images are visualized using a pre-defined color pallete 
    from the geocore.palette library
    """
    try:
        # Isolate the NIR and RED band components and add them to a dictionary
        values = {"NIR": image.select('B8'), "RED": image.select('B4')}
        # Generate the NDVI image and rename the resultant band
        ndvibase = image.expression("(NIR-RED)/(NIR+RED)", values).rename('NDVI')
        
    except ee.EEException as e:
        raise RuntimeError(f"ndvi composition failed. {e}")

    try:
        # Upsample the NDVI image with bicubic interpolation
        upsampled = ndvibase.resample('bicubic')
        # Reproject the upsampled image to the EPSG:4326 CRS
        upsampled = upsampled.reproject(crs="EPSG:4326", scale=1)
    
    except ee.EEException as e:
        raise RuntimeError(f"ndvi upsampling failed. {e}")

    try:
        # Scale each pixel value in the image by one order of magnitude
        ndvi = ee.Image(upsampled).toFloat().multiply(10).toInt().toFloat()
        # Focalize the image with a morpohological reducer
        ndvi = ndvi.focal_median(kernelType="square", radius=5)

    except ee.EEException as e:
        raise RuntimeError(f"ndvi focalization failed. {e}")

    try:
        # Apply the visualization pallete on the image
        visualized = ndvi.visualize(**pallete.NDVIFOCAL)

    except ee.EEException as e:
        raise RuntimeError(f"ndvi visualization failed. {e}")

    # Return the final NDVI image
    return visualized
