"""
Utility functions used to load and save Geopackage data and to extract the
CRS from GeoDataFrame instances.
"""
import geopandas
import pyproj


def load_geopackage(path: str) -> geopandas.GeoDataFrame:
    """
    Load a geopackage from the disk and return a `GeoDataFrame` instance of
    the loaded file. This method does not check if the input path exists and
    will raise a `DriverError` exception if the input path does not exist.

    :param path: Path to the input file to load
    :type path: str

    :return: `geopandas.GeoDataFrame`
    """
    return geopandas.read_file(path)


def save_geopackage(path: str, data: geopandas.GeoDataFrame) -> None:
    """
    Save a `GeoDataFrame` to the disk at the specified path. If the path
    already exists, the existing destination will be overwritten.

    :param path: Path used for the output file
    :type path: str

    :param data: Output `GeoDataFrame` instance
    :type data: GeoDataFrame
    """
    for row in data.itertuples():
        data.to_file(path, driver="GPKG", layer=row.name)


def validate_crs(data: geopandas.GeoDataFrame) -> bool:
    """
    Validate that a `GeoDataFrame` has a valid CRS for our purposes. In our
    case, the CRS needs to be a geographic CRS.

    :param data: `GeoDataFrame` to validate
    :type data: `GeoDataFrame`

    :return: True if the CRS is an instance of a geographic CRS
    """
    return data.crs.is_geographic


def extract_crs_geod(data: geopandas.GeoDataFrame) -> pyproj.Geod:
    """
    Create a `Geod` instance using the properties of the CRS of the input
    GeoDataFrame.

    :param data: input `GeoDataFrame` used to extract the CRS
    :type data: `GeoDataFrame`

    :return: `pyproj.Geod` using the input data CRS
    """
    return pyproj.Geod(
        a=data.crs.ellipsoid.semi_major_metre,
        rf=data.crs.ellipsoid.inverse_flattening,
    )
