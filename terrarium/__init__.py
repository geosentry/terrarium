"""
Terrarium Package
"""
import os
import ee

def initialize(project: str):
    """
    A function that initializes an Earth Engine session with the credentials 
    of a Service Account Agent. The Service Account must be authenticated to use 
    the Earth Engine API and the credentials must be provided as bytes string.
    """
    # Check if Earth Engine is already intialized
    if ee.data._initialized:
        return

    try:
        # Retrieve the location of the credentials file from the environment variable
        keyfile = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        # Construct the Service Account Credentials from the credentials bytes string
        eecredentials = ee.ServiceAccountCredentials(email=None, key_file=keyfile)

        # Use the Service Account Credentials and the project ID
        # to authenticate with Earth Engine and initialize the session
        ee.Initialize(credentials=eecredentials, project=project)

    except KeyError as e:
        raise RuntimeError(f"could not initalize earth engine. cannot find credentials")

    except Exception as e:
        raise RuntimeError(f"could not initialize earth engine. error: {e}")
