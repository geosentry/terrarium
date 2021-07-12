"""
Terrarium Package
"""

def initialize(credentials: bytes):
    """
    A function that initializes an Earth Engine session with the credentials 
    of a Service Account Agent. The Service Account must be authenticated to use 
    the Earth Engine API and the credentials must be provided as bytes string.
    """
    import ee

    # Check if Earth Engine is already intialized
    if ee.data._initialized:
        return

    # Check if the credentials are of the correct type
    if not isinstance(credentials, bytes):
        raise RuntimeError("could not initialize earth engine. credentials must be a byte string.")

    try:
        # Construct the Service Account Credentials from the credentials bytes string
        eecredentials = ee.ServiceAccountCredentials(email=None, key_data=credentials)
        # Use the Service Account Credentials to authenticate 
        # with Earth Engine and initialize the session
        ee.Initialize(credentials=eecredentials)

    except Exception as e:
        raise RuntimeError(f"could not initialize earth engine. error: {e}")
