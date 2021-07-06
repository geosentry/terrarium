"""
Terrarium Package

The spatial module contains function required 
for geometrical and spatial manipulations.
"""
import ee
import json

def generate_geometry(geojson: str) -> ee.Geometry:
    """ A function that returns an Earth Engine Geometry for a given GeoJSON string. """
    try:
        geodata = json.loads(geojson)
        coordinates = geodata['features'][0]['geometry']['coordinates'][0]

    except KeyError as e:
        raise RuntimeError(f"corrupt geojson. missing key {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"could not parse geojson. {e}")

    try:
        geometry = ee.Geometry.Polygon(coordinates)
        return geometry

    except Exception as e:
        raise RuntimeError(f"could not construct ee.Geometry. {e}")

def filter_coverage(collection: ee.ImageCollection, geometry: ee.Geometry) -> ee. ImageCollection:
    """
    A function that returns an Earth Engine ImageCollection that has been filtered such that every 
    Image in a given ImageCollection has full coverage for a given Earth Engine Geometry.

    This coverage filter is performed by assigning a coverage value to each image 
    which is value between 0-100 that represents the percentage of geometry coverage 
    in that image. The collection is then filtered based on this value.
    """
    # Assign a coverage value to each Image in the ImageCollection
    collection = collection.map(lambda image: image.set({
        "coverage": ee.Number.expression("100-(((expected-actual)/expected)*100)", {
            "expected": geometry.area(5), 
            "actual": image.clip(geometry).geometry().area(5)
        })
    }))

    # Filter the collection to only have Images with 100% coverage
    collection = collection.filter(ee.Filter.eq("coverage", 100))
    # Return the filtered collection
    return collection
