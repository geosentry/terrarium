"""
Terrarium Package

The spatial module contains function required 
for geometrical and spatial manipulations.
"""
import ee
import json
import shapely.geometry as shapes

def generate_earthengine_geometry(geojson: str) -> ee.Geometry:
    """ A function that returns an Earth Engine Geometry for a given GeoJSON string. """
    try:
        geodata = json.loads(geojson)
        coordinates = geodata['features'][0]['geometry']['coordinates'][0]

    except KeyError as e:
        raise RuntimeError(f"corrupt geojson. missing key: {e}.")
    except IndexError:
        raise RuntimeError(f"corrupt geojson. missing feature or coordinates.")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"could not parse geojson. {e}.")

    try:
        geometry = ee.Geometry.Polygon(coordinates)
        return geometry

    except Exception as e:
        raise RuntimeError(f"could not construct ee.Geometry. {e}")

def generate_shapely_geometry(geojson: str) -> shapes.shape:
    """ A function that returns a Shapely Geometry for a given GeoJSON string. """
    try:
        geodata = json.loads(geojson)
        geometry = geodata['features'][0]['geometry']

    except KeyError as e:
        raise RuntimeError(f"corrupt geojson. missing key: {e}")
    except IndexError:
        raise RuntimeError(f"corrupt geojson. missing feature.")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"could not parse geojson. {e}")

    try:
        shape = shapes.shape(geometry)
        return shape

    except Exception as e:
        raise RuntimeError(f"could not construct shapely geometry. {e}")

def generate_shapely_geojson(shape: shapes.shape) -> str:
    """ A function that returns a GeoJSON string for a given Shapely Geometry. """
    if not isinstance(shape, shapes.shape):
        raise RuntimeError("could not generate geojson. not a shapely shape")

    try:
        geojson = shapes.mapping(shape)
        return json.dumps(geojson)

    except Exception as e:
        raise RuntimeError(f"could not generate geojson. error: {e}")

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

def reshape_polygon(shape: shapes.Polygon) -> shapes.Polygon:
    """ A function that reshapes a Shapely Polygon into it's Square Bounding Box Polygon. """
    if not isinstance(shape, shapes.Polygon):
        raise RuntimeError("could not reshape polygon. not a shapely polygon")

    try:
        from math import sqrt

        # Retrieve the bounding coordinates
        minx, miny, maxx, maxy = shape.bounds
        # Calculate the polygon centroid
        centroid = [(maxx+minx)/2, (maxy+miny)/2]
        # Calculate the polygon diagonal
        diagonal = sqrt((maxx-minx)**2+(maxy-miny)**2)

    except Exception as e:
        raise RuntimeError(f"could not reshape polygon. could not calculate polygon metrics. error: {e}")

    try: 
        # Create Point shape at the centroid
        centroid = shapes.Point(centroid)
        # Buffer the centroid point shape as a square (cap style = 3)
        buffered = centroid.buffer(diagonal/2, cap_style=3)
        # Return the reshaped polygon
        return buffered
    
    except Exception as e:
        raise RuntimeError(f"could not reshape polygon. error: {e}")

def reshape_point(shape: shapes.Point, buffer: int = 2.5) -> shapes.Polygon:
    """ 
    A function that reshapes a Shapely Point into it's Square Bounding Box Polygon. 
    Creates a buffer around the point (2.5 kms by default).
    """
    if not isinstance(shape, shapes.Point):
        raise RuntimeError("could not reshape point. not a shapely point.")

    try:
        # Extract lat and lon values of the point
        lon, lat = shape.coords[:][0]
        # Create the Azimuthal Equidistant Projection string
        aeqd_proj = f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0"

    except Exception as e:
        raise RuntimeError(f"could not reshape point. could not calculate point metrics. error: {e}.")

    try:
        import pyproj
        from functools import partial
        from shapely.ops import transform

        # Construct the projection partial
        projection = partial(
            pyproj.transform, 
            pyproj.Proj(aeqd_proj), 
            pyproj.Proj('+proj=longlat +datum=WGS84')
        )

    except Exception as e:
        raise RuntimeError(f"could not reshape point. could not construct projecttion partial. error: {e}.")

    try: 
        # Create an arbitrary point and buffer it as a square
        buffered = shapes.Point(0, 0).buffer(buffer * 1000, cap_style=3)
        # Transform the arbitrary point with the projection partial
        buffered = transform(projection, buffered)
        # Return the reshaped point as polygon
        return buffered

    except Exception as e:
        raise RuntimeError(f"could not reshape point. error: {e}.")

def reshape_linestring(shape: shapes.LineString) -> shapes.Polygon:
    """ A function that reshapes a Shapely Polygon into it's Square Bounding Box Polygon. """
    if not isinstance(shape, shapes.LineString):
        raise RuntimeError("could not reshape linestring. not a shapely linestring")

    try:
        # Create the envelope polygon of the linestring
        envelope = shape.envelope
        # Reshape the envelope and return it.
        return reshape_polygon(envelope)

    except Exception as e:
        raise RuntimeError(f"could not reshape linestring. error: {e}.")
