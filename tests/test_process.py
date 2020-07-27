"""
Unit tests for the `utils` module
"""
# pylint: disable=redefined-outer-name
import os

import pytest
from shapely import geometry

from spike_removal import process, utils


class TestAngles:
    """Test suite for angular operations"""

    def test_90_degree_angle(self):
        """Test that an angle is a 90 degree angle"""
        assert process.get_angle_between_azimuths(0, 90) == 90

    def test_0_degree_angle(self):
        """Test that an angle is a 0 degree angle"""
        assert process.get_angle_between_azimuths(0, 0) == 0

    def test_angle_is_wrapped(self):
        """Test that an angle is wrapped around the 180 degree angle"""
        assert process.get_angle_between_azimuths(0, 270) == 90

    def test_known_angle(self):
        """Test against a know angle"""
        assert process.get_angle_between_azimuths(10, -15) == 25


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
