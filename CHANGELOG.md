# Terrarium Changelog

**Current Version: v0.2.4**

## v0.4

### v0.4.0
- Reworked the reshape functions in the spatial module to work with projections that are distorted because of their distance from the equator.
- The API key for the Maps Platform functionality is now stored in an environment variable 'MAPS_APIKEY'. Changed from 'MAPS_GEOCODING_APIKEY'.
- Fixed issues with exported image distortions caused by the ``generate_spectral_image`` function because it was reprojecting to EPSG:4326 instead of the native CRS for the latitude and longitude based on the geometry of the image region.
- Reworked the export module to use the projection of the Image while exporting. The function also requires a bucket name now.
- Added a function to retrieve the status of an export task from a task ID and the project ID.

## v0.3

### v0.3.2
- Refactored inputs on all modules to be top level gloabl imports
- Rebuilt the spectral module to be more aligned with the requirements of geocore-spectral. The module now contains a set of mappable algorithms that apply the spectral transformation on all images in a collection. These algorithms and the palettes are used in conjunction with a function ``generate_spectral_image`` that accepts a datetime, an ee.Geometry and the ID of the spectral index to generate. It isolates the images for the geometry and 12 hour buffer around the given date and transforms all images in that collection with the algorithm before combining them with a mosiac function and clipping it to the geometry and applying visualization parameters.

### v0.3.1
- Updated temporal module function interfaces.
- Unified the daterange and datebuffer functionality
- Added error handling blocks for complex temporal module functions.
- Renamed pallete module to palette (Spelling Fix) and renamed ``S2TC`` palette to ``S2TRUECOLOR``.
- Renamed ``generate_locarion`` to ``generate_location`` (Spelling Fix).
- Removed the ``filter_coverage`` function from the spatial module.
- Removed the acquisition module.

### v0.3.0
- Refactored the Earth Engine Initialization Runtime. The initialization function now accepts a credentials string and does not concern itself with how the credentials are obtained and is left upto the runtime that calls it.
- Removed the dependency on Secret Manager. 
- Initialization Runtime is now idempotent and can be called multiple times without creating new sessions each time.

## v0.2

### v0.2.4
- Updated spatial module function interfaces.
- Added support for centroid generation.
- Added support for reverse geocoding address lookup using the **Google Maps Geocoding API**

### v0.2.3
- Fixed issues with calculated area value truncation.

### v0.2.2
- Added support for geometry area calculation in multiple units.

### v0.2.1
- Added more advanced spatial manipulations with the **Shapely** and **PyProj** packages for shape and projection manipulation.
- Added support for bound based geometries and geometry reshaping.

### v0.2.0
- **Terrarium** package exists in a functional state with a full set of modules that handle spatio-temporal manipulations and generations, Earth Engine exports, visualization palletes and spectral manipulation for TC and NDVI indices.

## v0.1

### v0.1.0
- **Terrarium** Git Repository Initialized with setup tools and configuration
- Package functionality is limited to the acquisition module ported from the previous configuration.

### v0.0.0
- The package is refered to as the **geocore** package and exists as a subpackage of a cloud function in the **geosentry/eventhandlers** repository.
- Contains simple functions for generating NDVI, exporting assets and conveting image types. All non-GIS and Earth Engine related functionality was removed.