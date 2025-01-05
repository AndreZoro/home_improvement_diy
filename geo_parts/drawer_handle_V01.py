import io
import tempfile
import os
from build123d import *


def create_handle(
    h_width=90,
    h_thickness=35,
    h_height=5,
    b_width=50,
    b_thickness=20,
    b_height=20,
    screw_dia=4,
    screw_distance=50,
    sid='bla'
):

    screw_dpt = h_height + b_height - 1
    handle_champfer_l = h_height / 4
    fillet_rad = (h_thickness - b_thickness) / 6


    messages = []

    if screw_dpt <= screw_dia:
        messages.append("There is only very little screw depth. Try increasing either the base or the handle height.")

    if (b_height-(screw_dia * 1.8)) <= 0.1 * b_height:
        messages.append("The base is pretty thin for the selected screw. Try either using a smaller screw or better increase the base height.")


    # base lines
    l1 = Line((-b_width / 2, b_thickness / 2), (b_width / 2, b_thickness / 2))
    l2 = ThreePointArc(
        (b_width / 2, b_thickness / 2),
        (b_width / 2 + b_thickness / 2, 0),
        (b_width / 2, -b_thickness / 2),
    )
    l3 = Line((b_width / 2, -b_thickness / 2), (-b_width / 2, -b_thickness / 2))
    l4 = ThreePointArc(
        (-b_width / 2, -b_thickness / 2),
        (-b_width / 2 - b_thickness / 2, 0),
        (-b_width / 2, b_thickness / 2),
    )

    base_lines = l1 + l2 + l3 + l4
    base_sk = make_face(base_lines)
    base_body = extrude(base_sk, -b_height)

    # handle lines
    l1 = Line((-h_width / 2, h_thickness / 2), (h_width / 2, h_thickness / 2))
    l2 = ThreePointArc(
        (h_width / 2, h_thickness / 2),
        (h_width / 2 + h_thickness / 2, 0),
        (h_width / 2, -h_thickness / 2),
    )
    l3 = Line((h_width / 2, -h_thickness / 2), (-h_width / 2, -h_thickness / 2))
    l4 = ThreePointArc(
        (-h_width / 2, -h_thickness / 2),
        (-h_width / 2 - h_thickness / 2, 0),
        (-h_width / 2, h_thickness / 2),
    )

    h_lines = l1 + l2 + l3 + l4
    h_sk = make_face(h_lines)
    h_body = extrude(h_sk, h_height)
    h_body = chamfer(h_body.edges(), length=handle_champfer_l)

    base_handle = h_body + base_body

    # base_plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1]) * Pos(
    #        -7 / 2 + 1.5 * 4, -4 / 2, 0
    #    )

    base_plane_screw_hole = Plane(base_handle.faces().sort_by(Axis.Z)[0])
    base_handle -= (
        base_plane_screw_hole
        * Pos(screw_distance / 2, 0, 0)
        * CounterSinkHole(
            radius=screw_dia / 2,
            counter_sink_radius=(screw_dia / 2) * 1.25,
            depth=screw_dpt,
        )
    )
    base_handle -= (
        base_plane_screw_hole
        * Pos(-screw_distance / 2, 0, 0)
        * CounterSinkHole(
            radius=screw_dia / 2,
            counter_sink_radius=(screw_dia / 2) * 1.25,
            depth=screw_dpt,
        )
    )

    base_handle = fillet(base_handle.edges().filter_by(Axis.X)[7], radius=fillet_rad)

    part_file_name = f"drawer_handle_{sid}.stl"
    fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])
    os.close(fd)
    export_stl(base_handle, temp_file_name)

    if len(messages) == 0:
        messages.append("Part generated successfully.")

    return temp_file_name, messages


