"""Utilities
"""
import geopandas
import pyproj


def load_geopackage(path: str) -> geopandas.GeoDataFrame:
    """Load a geopackage from the disk and return a `GeoDataFrame` instance of
    the loaded file.

    :param path: Path to the input file to load
    :type path: str

    :return: Loaded GeoDataFrame
    """
    return geopandas.read_file(path)


def save_geopackage(path: str, data: geopandas.GeoDataFrame) -> None:
    """Save a `GeoDataFrame` to the disk at the specified path

    :param path: Path used for the output file
    :type path: str

    :param data: Output `GeoDataFrame` instance
    :type data: GeoDataFrame
    """
    raise NotImplementedError


def validate_crs(data: geopandas.GeoDataFrame) -> bool:
    """Validate that a GeoDataFrame has a valid CRS for our purposes. In our
    case, the CRS needs to be a geographic CRS.

    :param data: GeoDataFrame to validate
    :type data: GeoDataFrame

    :return: True if the CRS is an instance of a geographic CRS
    """
    return data.crs.is_geographic


def extract_crs_geod(data: geopandas.GeoDataFrame) -> pyproj.Geod:
    """Create a `Geod` instance using the properties of the CRS of the input
    GeoDataFrame.

    :param data: input GeoDataFrame
    :type data: GeoDataFrame

    :return: Geod using the input data CRS
    """
    return pyproj.Geod(
        a=data.crs.ellipsoid.semi_major_metre,
        rf=data.crs.ellipsoid.inverse_flattening,
    )
