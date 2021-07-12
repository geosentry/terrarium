# Terrarium
![Banner](banner.jpg)

### **Terrarium** is a Python Package that contains the **Earth Engine** and **GIS** related tooling for the **GeoSentry** 🌍 Platform.

**Version: 0.2.4**  
**Language: Python 3.9**  
**License: MIT**  
**Status: In Development**  

## Overview
**GeoSentry** is a geospatial observation platform with spectral, topographical and comparative analytics along with a community-curated gallery of stunning satellite imagery powered by ESA's **Sentinel-2** & **Google Earth Engine**.

### Google Earth Engine
**Terrarium** uses the [Earth Engine Python API](https://github.com/google/earthengine-api) for much of its geospatial manipulation functionality and satellite imagery datasources. Google Earth Engine is a planetary-scale platform for Earth science data & analysis that is powered by Google's Cloud Infrastructure and integrates well with Google Cloud Platform.

### Satellite Sources
**Terrarium** is mostly confined to using the European Space Agency's **Sentinel-2 MSI Level-2A** dataset which is corrected for *Surface Reflectance* and available within the Earth Engine Data Catalog with the Collection ID ``COPERNICUS/S2_SR``. The multi-spectral bands of the dataset are used for spectral index generation and false color compositions.  

The *Truecolor* bands available to the L2A collection is also used for generation images, while the SCL band is used for rendering the *Scene Classification Layer* as part of **GeoSentry's** topographical analysis.

Cloudiness values are generated using *Sentinel-2 Cloud Probability* dataset which is also available on the Earth Engine Catalog with the Collection ID ``COPERNICUS/S2_CLOUD_PROBABILITY``.

**Terrarium** also uses JAXA's **ALOS DSM** dataset for altitude based topographical analysis. The dataset is available with the Collection ID ``JAXA/ALOS/AW3D30/V3_2``.

### Asset Generation
!todo


## Installation
The package can be installed with ``pip`` using the following command.
```shell
pip install git+https://github.com/geosentry/terrarium#egg=terrarium
```

A specific version of the package can also be installed. The ``v0.2.0`` tag can be installed using
```shell
pip install git+https://github.com/geosentry/terrarium.git@v0.2.0#egg=terrarium
```
### Authentication
The package requires setup for authentication with services such as Google Earth Engine and Google Maps Platform.

#### Google Earth Engine
Authentication for the Google Earth Engine API is done using a GCP IAM Service Account.

1. A Service Account needs to be created and registered with Earth Engine as specified in https://developers.google.com/earth-engine/guides/service_account. 
2. This Service Account needs the ``Storage Object Admin`` IAM role to perform exports to a Cloud Storage Bucket.
3. Currently the credentials are retrieved from **Secret Manager**, but this flow will be modified in v0.3

#### Google Maps Geocoding API
Authenticating with Google Maps Geocoding API is done using an API Key.

1. Create an API Key with steps specified in https://developers.google.com/maps/gmp-get-started#create-project.
2. Restrict the API Key for usage with the Geocoding API
3. Store the API Key as environment variable ``MAPS_GEOCODING_APIKEY``.

### Changelog
The package changelog is located in the CHANGELOG.md file in the root directory of the repository.
