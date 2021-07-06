"""
Terrarium Package
"""
import ee
import google.cloud.secretmanager as secretmanager

# from . import pallete
# from . import temporal
# from . import spatial
# from . import spectral
# from . import acquisition
# from . import export

def initialize(project: str):
    """
    A function that initializes an Earth Engine session with a Service Account Agent.
    The credentials of the Service Account are stored on GCP Secret Manager.
    """
    try:
        # Create a client for the Secret Manager Service.
        secrets = secretmanager.SecretManagerServiceClient()
    
    except Exception as e:
        raise RuntimeError(f"unable to initialize a secret manager client - {e}")

    try:
        # Construct the name of the earth engine secret
        secret_name = f"projects/{project}/secrets/earthengineone/versions/latest"
        # Access the secret data using the secret name
        secret_data = secrets.access_secret_version(name=secret_name)

    except Exception as e:
        raise RuntimeError(f"unable to access earth engine secret - {e}")

    try:
        # Construct the Service Account Credentials from the secret data
        eecredentials = ee.ServiceAccountCredentials(email=None, key_data=secret_data.payload.data)
        # Use the Service Account Credentials to authenticate the Earth Engine Session
        ee.Initialize(credentials=eecredentials)

    except Exception as e:
        raise RuntimeError(f"unable to initialize earth engine session - {e}")
