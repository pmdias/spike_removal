"""Geometry processing with methods for spike removal
"""
import pyproj
from shapely import coords


def get_angle_between_azimuths(azimuth1, azimuth2) -> float:
    """Get the angle between two azimuths.

    :param azimuth1: The first azimuth angle
    :type azimuth1: float

    :param azimuth2: The second azimuth angle
    :type azimuth2: float

    :return: Angle between the given azimuths
    """
    tmp = abs(azimuth1 - azimuth2) % 360
    return 360 - tmp if tmp > 180 else tmp


class GeometryProcessor:
    """Processor used to ingest a geometry as a sequence of geographic
    coordinates and remove spikes.
    """
    min_angle: float = 1.0
    min_distance: float = 100000.0

    def __init__(self, min_angle: float, min_distance: float):
        self.min_angle = min_angle % 360
        self.min_distance = abs(min_distance)

    def process_sequence(
            self,
            geod: pyproj.Geod,
            sequence: coords.CoordinateSequence
    ) -> list:
        """Process a sequence of coordinate points and remove all spikes.

        :param geod: Geod used to perform distance and angle calculations
        :type geod: pyproj.Geod

        :param sequence: input coordinate sequence
        :type sequence: CoordinateSequence

        :return: Filtered list with the spikes removed from the input sequence
        """
        if len(sequence) <= 4:
            # If the number of points in the coordinate sequence is 4 or less,
            # this means that the sequence is a triangle and it means that we
            # don't want to process this at the risk of creating an invalid
            # polygon geometry
            return list(sequence)

        vertices = sequence[:-1]  # discard the last vertex
        triplets = [
            ((i - 1) % len(vertices), i, (i + 1) % len(vertices))
            for i in range(len(vertices))
        ]

        final_geometry = []

        for triplet in triplets:
            mark = self.process_triplet(geod, [
                vertices[triplet[0]],
                vertices[triplet[1]],
                vertices[triplet[2]],
            ])

            if not mark:
                final_geometry.append(vertices[triplet[1]])

        return final_geometry

    def process_triplet(self, geod: pyproj.Geod, triplet: list) -> bool:
        """Process a triplet of vertices and check if the second vertex can be
        marked as a spike.

        :param geod: Geod used to perform distance and angle calculations
        :type geod: pyproj.Geod

        :param triplet: List with 3 vertices
        :type triplet: list

        :return: True if the second vertex is a spike
        """
        azim10, _, distance10 = geod.inv(*triplet[1], *triplet[0])
        azim12, _, distance12 = geod.inv(*triplet[1], *triplet[2])

        if distance10 < self.min_distance and distance12 < self.min_distance:
            return False

        angle = get_angle_between_azimuths(azim10, azim12)
        if angle < self.min_angle:
            return True

        return False
