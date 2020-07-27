"""
Command line entrypoint
"""
import click
from geopandas import GeoDataFrame
from shapely.geometry import Polygon

from . import utils, process


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--angle", default=1.0, help="""
    Maximum angle, in degrees, used to evaluate spikes. Defaults to 1.0º.""")
@click.option("--distance", default=100000.0, help="""
    Minimum distance, in meters, used to evaluate spikes. Defaults to 100 000m
    """)
@click.option("-o", "--output", required=True, help="""
    Name of the output destination file""")
def main(filename: str, angle: float, distance: float, output: str):
    """
    A command-line tool used to remove spikes from polygons stored in
    Geopackage format.
    """
    data = utils.load_geopackage(filename)

    if not utils.validate_crs(data):
        raise Exception("Not a valid geographic CRS")

    geod = utils.extract_crs_geod(data)

    processor = process.GeometryProcessor(angle, distance)

    results = []

    for entry in data.itertuples():
        geometry = entry.geometry

        exterior = processor.process_sequence(geod, geometry.exterior.coords)

        results.append((entry.name, Polygon(exterior)))

    out = GeoDataFrame(results, columns=["name", "geometry"], crs=data.crs)

    for result in results:
        out.to_file(output, layer=result[0], driver="GPKG")
