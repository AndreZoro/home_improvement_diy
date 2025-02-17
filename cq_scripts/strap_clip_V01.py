# import build123d as bd
from build123d import *
import io
import tempfile
import os


width = 35
thickness = 3
height = 55
layer_width = 0.4
n_shells = 3


def build_strap_clip(
    width=20, thickness=3, height=22, layer_width=0.4, n_shells=3, sid="none"
):
    msgs = []
    shell_thickness = layer_width * n_shells
    if shell_thickness <= 0.1:
        shell_thickness = 0.2
        msgs.append(
            f"With current settings, the shell thickness is to low. Automatically increased to :{shell_thickness:.3f}mm. Check you shell count and layer width."
        )

    if width < thickness * 1.5:
        width = thickness * 1.5
        msgs.append(
            f"Width automatically increased to {width:.3f}mm. Check you chosen width, it is a bit narrow for the selected strap thickness."
        )

    # Inner lines
    l1 = Line(
        (-(width - thickness) / 2, thickness / 2),
        ((width - thickness) / 2, thickness / 2),
    )
    l2 = ThreePointArc(
        ((width - thickness) / 2, thickness / 2),
        (width / 2, 0),
        ((width - thickness) / 2, -thickness / 2),
    )
    l3 = Line(
        ((width - thickness) / 2, -thickness / 2),
        (-(width - thickness) / 2, -thickness / 2),
    )
    l4 = ThreePointArc(
        (-(width - thickness) / 2, -thickness / 2),
        (-width / 2, 0),
        (-(width - thickness) / 2, thickness / 2),
    )

    inner_lines = l1 + l2 + l3 + l4
    inner_sk = make_face(inner_lines)
    inner_body = extrude(inner_sk, height)

    # Outer lines
    ll1 = Line(
        (-(width - thickness) / 2, thickness / 2 + shell_thickness),
        ((width - thickness) / 2, thickness / 2 + shell_thickness),
    )
    ll2 = ThreePointArc(
        ((width - thickness) / 2, thickness / 2 + shell_thickness),
        ((width / 2) + shell_thickness, 0),
        ((width - thickness) / 2, -thickness / 2 - shell_thickness),
    )
    ll3 = Line(
        ((width - thickness) / 2, -thickness / 2 - shell_thickness),
        (-(width - thickness) / 2, -thickness / 2 - shell_thickness),
    )
    ll4 = ThreePointArc(
        (-(width - thickness) / 2, -thickness / 2 - shell_thickness),
        ((-width / 2) - shell_thickness, 0),
        (-(width - thickness) / 2, thickness / 2 + shell_thickness),
    )

    outer_lines = ll1 + ll2 + ll3 + ll4
    outer_sk = make_face(outer_lines)
    outer_body = extrude(outer_sk, height)

    main_body = outer_body - inner_body

    ref_slot_width = (width - thickness) / 2
    slot_thickness = min(thickness / 2, ref_slot_width / 4)
    print(f"Slot thickness: {slot_thickness:.3f} - \t ref width: {ref_slot_width:.3f}")

    """
    plane = Plane(main_body.faces().sort_by(Axis.Y)[0]) * Pos(
        -ref_slot_width + slot_thickness*1.6, -height / 2, 0
    )
    """

    plane = Plane(main_body.faces().sort_by(Axis.Y)[0]) * Pos(0, -height / 2, 0)
    delta_x = -(ref_slot_width * 0.96 - slot_thickness * 1.2)
    delta_x = -((width - thickness) / 2 - slot_thickness * 1.6 - ref_slot_width / 6)

    pts = [
        (0 + delta_x, 0),  # 0
        (0 + delta_x, height / 3),  # 1
        ((-ref_slot_width / 6) + delta_x, height * 2 / 3),  # 2
        ((-ref_slot_width / 6) + delta_x, height),  # 3
        ((-ref_slot_width / 6) + delta_x + 1 * slot_thickness, height),  # 4
        ((-ref_slot_width / 6) + delta_x + 1 * slot_thickness, height * 2 / 3),  # 5
        ((1 * slot_thickness) + delta_x, height / 3),  # 6
        ((1 * slot_thickness) + delta_x, 0),  # 7
        (0 + delta_x, 0),
        0,  # 0
    ]

    slot_lines = Polyline(pts)

    slot_sk = plane * make_face(slot_lines)
    main_body -= extrude(slot_sk, -shell_thickness)

    try:
        main_body = fillet(main_body.edges().filter_by(Axis.Y)[-4:], radius=thickness)
    except:
        msgs.append(
            "Was not able to round the corners in the slot gap. Maybe you are using strange dimensions?"
        )

    if n_shells >= 3:
        try:
            last_edges = main_body.edges().group_by(Axis.Y)[-1]
            main_body = chamfer(last_edges, length=shell_thickness / 2.5)
        except:
            msgs.append(
                "Was not able to champfer the outer edges. Maybe you are using strange dimensions?"
            )

    part_file_name = f"strap_clip_{sid}.stl"

    if len(msgs) == 0:
        msgs.append("Successfully created part.")

    return main_body


geo_part = build_strap_clip(width, thickness, height, layer_width, n_shells)

show_object(geo_part)
