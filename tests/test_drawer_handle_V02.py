import pytest
from itertools import product
import random

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../geo_parts"))
)

import build123d as bd

from drawer_handle_V02 import create_build123d_handle_v02

# Configuration for parameter ranges
# PARAM_RANGES = {
#     "h_width": {"min": 10, "max": 400, "step": 1},
#     "h_thickness": {"min": 1, "max": 20, "step": 0.5},
#     "h_height": {"min": 10, "max": 130, "step": 1},
# }

PARAM_RANGES = {
    "h_width": {"min": 10, "max": 140, "step": 65},
    "h_thickness": {"min": 1, "max": 20, "step": 9.5},
    "h_height": {"min": 10, "max": 60, "step": 30},
    "h_rad": {"min": 0, "max": 100, "step": 50},
    "b_thickness": {"min": 2, "max": 40, "step": 20},
    "screw_distance": {"min": 10, "max": 120, "step": 60},
    "screw_dia": ["m2", "m4", "m8"],
    "slant_ang": {"min": -45, "max": 45, "step": 45},
    "front_text": ["", "ms", "pretty awesome long text"],
}

# PARAM_RANGES = {
#     "h_width": {"min": 35, "max": 140, "step": 25},
#     "h_thickness": {"min": 16.0, "max": 20, "step": 7.5},
#     "h_height": {"min": 60, "max": 60, "step": 20},
#     "h_rad": {"min": 0, "max": 100, "step": 25},
#     "b_thickness": {"min": 2, "max": 40, "step": 10},
#     "screw_distance": {"min": 10, "max": 120, "step": 20},
#     "screw_dia": ["m2", "m4", "m8"],
#     "slant_ang": {"min": -45, "max": 45, "step": 22.5},
#     "front_text": ["",]# "ms",]# "pretty awesome long text"],
# }

# PARAM_RANGES = {
#     "h_width": {"min": 10, "max": 12, "step": 1},
#     "h_thickness": {"min": 1, "max": 3, "step": 1},
#     "h_height": {"min": 10, "max": 13, "step": 1},
# }


def generate_values(param_config):
    """Generate a range of values from a parameter configuration."""
    # breakpoint()
    if isinstance(param_config, dict):
        param_list = []
        min_val, max_val, step = (
            param_config["min"],
            param_config["max"],
            param_config["step"],
        )
        current = min_val
        while current <= max_val:
            param_list.append(current)
            # yield current
            current += step
        if max_val not in param_list:
            param_list.append(max_val)
        random.shuffle(param_list)
        return param_list
    else:
        # if it is a list:
        random.shuffle(param_config)
        return param_config


# # Generate all combinations of argument values
# ranges = [generate_values(PARAM_RANGES[param]) for param in PARAM_RANGES]
# all_combinations = list(product(*ranges))


def generate_combinations():
    """Lazily generate all combinations of parameter values."""
    ranges = (generate_values(PARAM_RANGES[param]) for param in PARAM_RANGES)
    for combination in product(*ranges):
        yield combination


# @pytest.mark.parametrize("h_width, h_thickness, h_height","h_rad","b_thickness","screw_distance","screw_dia","slant_ang","front_text", generate_combinations())
# def test_geometry_creation(h_width, h_thickness, h_height,h_rad,b_thickness,screw_distance,screw_dia,slant_ang,front_text,):


def test_geometry_creation():
    """Test the geometry creation function with all combinations."""
    combinations = generate_combinations()
    for combo in combinations:
        # breakpoint()
        try:
            # print(f"\nTesting combo: {h_width} - {h_thickness} - {h_height}")
            print(f"\nTesting combo: {combo}")
            geometry, _, _ = create_build123d_handle_v02(*combo, sid="test")
            # breakpoint()
            assert isinstance(
                geometry, bd.topology.Part
            ), f"Returned type is not Workplane for inputs ({h_width} - {h_thickness} - {h_height})"
            # assert geometry.is_manifold, ("Part is not manifold.")
            assert (
                len(geometry.solids()) == 1
            ), "Looks like we created multiple solids (maybe 0)"
        except Exception as e:
            breakpoint()
            pytest.fail(f"Exception raised for inputs ({combo}): {e}")
