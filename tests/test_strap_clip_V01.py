import pytest
from itertools import product
import random

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../geo_parts"))
)

import build123d as bd

from simple_strap_clip_V01 import build_build123d_strap_clip


PARAM_RANGES = {
    "width": {"min": 5, "max": 100, "step": 12},
    "thickness": {"min": 1, "max": 20, "step": 3},
    "height": {"min": 2, "max": 200, "step": 25},
    "layer_width": {"min": 0.01, "max": 1.0, "step": 0.1},
    "n_shells": {"min": 1, "max": 20, "step": 3},
}


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
            print(f"\nTesting Strap Clip V01 combo: {combo}")
            geometry, _, _ = build_build123d_strap_clip(*combo, sid="test")
            # breakpoint()
            assert isinstance(
                geometry, bd.topology.Part
            ), f"Returned type is not Workplane for inputs ({combo})"
            # assert geometry.is_manifold, ("Part is not manifold.")
            # assert len(geometry.solids())==1, ("Looks like we created multiple solids (maybe 0)")
        except Exception as e:
            breakpoint()
            pytest.fail(f"Exception raised for inputs ({combo}): {e}")
