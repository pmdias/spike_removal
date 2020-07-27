"""
Unit tests for the `utils` module
"""
# pylint: disable=redefined-outer-name
import os

import pytest
from shapely import geometry

from spike_removal import process, utils


@pytest.fixture
def simple_polygon_fixture():
    """Fixture for simple polygon"""
    test_directory = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(
        test_directory,
        "data/test_simple_polygons_data.gpkg"
    )

    return utils.load_geopackage(test_data_path)


@pytest.fixture
def polygon_with_holes():
    """Fixture for geometry with holes."""
    test_directory = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(
        test_directory,
        "data/test_polygon_holes_data.gpkg"
    )

    return utils.load_geopackage(test_data_path)


@pytest.fixture
def default_processor():
    """Fixture for the default GeometryProcessor"""
    return process.GeometryProcessor(1.0, 100000.0)


def test_polygon_without_spikes(simple_polygon_fixture, default_processor):
    """Test that the processing of a polygon without spikes returns the same
    polygon without any changes."""
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "no_spikes"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert polygon.equals(test_geom)


def test_polygon_multiple_spikes(simple_polygon_fixture, default_processor):
    """Test that a polygon with multiple spikes has all the spikes removed
    after processing."""
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "multiple_spikes"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert len(polygon.exterior.coords) == len(test_geom.exterior.coords) - 2


def test_polygon_single_criteria(simple_polygon_fixture, default_processor):
    """Test that a polygon with a spike that only meets one of the criteria
    used to mark spikes, is equal to the original polygon after processing."""
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "single_criteria"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert polygon.equals(test_geom)


def test_polygon_holes_no_spikes(polygon_with_holes, default_processor):
    """Test that a polygon with holes but no spikes is returned without any
    changes after being processed."""
    test_geom = (
        polygon_with_holes.loc[
            polygon_with_holes["name"] == "no_spikes"
        ]
        .geometry.values[0]
    )

    processed_rings = []

    for sequence in test_geom.interiors:
        vertices = default_processor.process_sequence(
            utils.extract_crs_geod(polygon_with_holes),
            sequence.coords
        )
        processed_rings.append(vertices)

    polygon = geometry.Polygon(test_geom.exterior, processed_rings)

    assert polygon.equals(test_geom)


def test_polygon_interior_spike(polygon_with_holes, default_processor):
    """Test that a polygon with a spike on a interior ring is returned without
    the internal spike after processing."""
    test_geom = (
        polygon_with_holes.loc[
            polygon_with_holes["name"] == "interior_spike"
        ]
        .geometry.values[0]
    )

    processed_rings = []

    for sequence in test_geom.interiors:
        vertices = default_processor.process_sequence(
            utils.extract_crs_geod(polygon_with_holes),
            sequence.coords
        )
        processed_rings.append(vertices)

    polygon = geometry.Polygon(test_geom.exterior, processed_rings)

    assert len(polygon.interiors[0].coords) == \
        len(test_geom.interiors[0].coords) - 1


def test_multiple_interior_spikes(polygon_with_holes, default_processor):
    """Test that a polygon with spikes in multiple interior rings is returned
    without any of the spikes after processing."""
    test_geom = (
        polygon_with_holes.loc[
            polygon_with_holes["name"] == "multiple_holes_with_spikes"
        ]
        .geometry.values[0]
    )

    processed_rings = []

    for sequence in test_geom.interiors:
        vertices = default_processor.process_sequence(
            utils.extract_crs_geod(polygon_with_holes),
            sequence.coords
        )
        processed_rings.append(vertices)

    polygon = geometry.Polygon(test_geom.exterior, processed_rings)

    assert (
        len(polygon.interiors[0].coords) ==
        len(test_geom.interiors[0].coords) - 1
    ) and (
        len(polygon.interiors[1].coords) ==
        len(test_geom.interiors[1].coords) - 1
    )


def test_90_degree_angle():
    """Test that an angle is a 90 degree angle"""
    assert process.get_angle_between_azimuths(0, 90) == 90


def test_0_degree_angle():
    """Test that an angle is a 0 degree angle"""
    assert process.get_angle_between_azimuths(0, 0) == 0


def test_angle_is_wrapped():
    """Test that an angle is wrapped around the 180 degree angle"""
    assert process.get_angle_between_azimuths(0, 270) == 90


def test_known_angle():
    """Test against a know angle"""
    assert process.get_angle_between_azimuths(10, -15) == 25
