# Terrarium Changelog

**Current Version: v0.2.4**

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