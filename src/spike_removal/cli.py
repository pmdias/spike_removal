"""
Command line entrypoint
"""
import click

from . import utils, process


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--angle", default=1.0, help="Angle")
@click.option("--distance", default=100000.0, help="Distance")
def main(filename: str, angle: float, distance: float):
    """
    spike_removal entrypoint
    """
    data = utils.load_geopackage(filename)

    if not utils.validate_crs(data):
        raise Exception("Not a valid geographic CRS")

    geod = utils.extract_crs_geod(data)

    processor = process.GeometryProcessor(angle, distance)
