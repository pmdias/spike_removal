"""
Unit tests for the `utils` module
"""
from spike_removal import process


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
