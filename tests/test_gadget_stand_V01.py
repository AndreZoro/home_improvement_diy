import pytest
from itertools import product
import random

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../geo_parts"))
)

import build123d as bd

from gadget_stand_v01 import build_stand


PARAM_RANGES = {
    "dev_w": {"min": 15, "max": 120, "step": 10},
    "dev_h": {"min": 30, "max": 220, "step": 40},
    "dev_t": {"min": 2, "max": 20, "step": 5},
    "slant": {"min": 10, "max": 40, "step": 10},
    "laptop_slot": [True, False],
    "laptop_thickness": {"min": 3, "max": 10, "step": 4},
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
            print(f"\nTesting Gadget Stand V01 combo: {combo}")
            geometry, _ = build_stand(*combo, sid="test")
            # breakpoint()
            assert isinstance(
                geometry, bd.topology.Part
            ), f"Returned type is not Workplane for inputs ({combo})"
            #assert geometry.is_manifold, ("Part is not manifold.")
            assert len(geometry.solids())==1, ("Looks like we created multiple solids (maybe 0)")
        except Exception as e:
            breakpoint()
            pytest.fail(f"Exception raised for inputs ({combo}): {e}")
