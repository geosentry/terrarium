# Terrarium
![Banner](banner.jpg)

### **Terrarium** is a Python Package that contains the **Earth Engine** and **GIS** related tooling for the **GeoSentry** 🌍 Platform.

**Version: 0.4.0**  
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


## Installation
The package can be installed with ``pip`` using the following command.
```shell
pip install git+https://github.com/geosentry/terrarium#egg=terrarium
```

A specific version of the package can also be installed. The ``v0.3.0`` tag can be installed using
```shell
pip install git+https://github.com/geosentry/terrarium.git@v0.3.0#egg=terrarium
```
### Authentication
The package requires authentication setup to use services such as Google Earth Engine and Google Maps Platform.

#### Google Earth Engine
Authentication for the Google Earth Engine API is done using a IAM Service Account.

1. A Service Account needs to be created and registered with Earth Engin. Refer to the [guide on creating and registering service accounts](https://developers.google.com/earth-engine/guides/service_account) for Earth Engine. 
2. Grant the ``Storage Object Admin`` IAM role to the Service Account. This allows it to perform exports to a Cloud Storage Bucket.
3. Generate a key for the Service Account and store it somewhere safe.
4. **Terrarium** requires the contents of this file as a bytes string to authenticate the Earth Engine Session.

#### Google Maps Platform
Authentication for the Google Maps APIs are done using an API Key. The **Terrarium** package currently uses the **Geocoding API** for reverse coding and address resolution. API Keys can be created with the steps specified in this [guide](https://developers.google.com/maps/gmp-get-started#create-project).

1. Create an API Key from the Google Cloud Platform Project
2. Store the API Key in the environment variable ``MAPS_APIKEY``.

## Changelog
The package changelog is located in the ``CHANGELOG.md`` file in the root directory of the repository.
