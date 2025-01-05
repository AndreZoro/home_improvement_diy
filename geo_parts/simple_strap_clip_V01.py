# import build123d as bd
from build123d import *
import io
import tempfile
import os


def build_strap_clip(width=20, thickness=3, height=22, layer_width=0.4, n_shells=3,sid='none'):
    shell_thickness = layer_width * n_shells

    # Inner lines
    l1 = Line((-width / 2, thickness / 2), (width / 2, thickness / 2))
    l2 = ThreePointArc(
        (width / 2, thickness / 2),
        (width / 2 + thickness / 2, 0),
        (width / 2, -thickness / 2),
    )
    l3 = Line((width / 2, -thickness / 2), (-width / 2, -thickness / 2))
    l4 = ThreePointArc(
        (-width / 2, -thickness / 2),
        (-width / 2 - thickness / 2, 0),
        (-width / 2, thickness / 2),
    )

    inner_lines = l1 + l2 + l3 + l4
    inner_sk = make_face(inner_lines)
    inner_body = extrude(inner_sk, height)

    # Outer lines
    ll1 = Line(
        (-width / 2, thickness / 2 + shell_thickness),
        (width / 2, thickness / 2 + shell_thickness),
    )
    ll2 = ThreePointArc(
        (width / 2, thickness / 2 + shell_thickness),
        (width / 2 + thickness / 2 + shell_thickness, 0),
        (width / 2, -thickness / 2 - shell_thickness),
    )
    ll3 = Line(
        (width / 2, -thickness / 2 - shell_thickness),
        (-width / 2, -thickness / 2 - shell_thickness),
    )
    ll4 = ThreePointArc(
        (-width / 2, -thickness / 2 - shell_thickness),
        (-width / 2 - thickness / 2 - shell_thickness, 0),
        (-width / 2, thickness / 2 + shell_thickness),
    )

    outer_lines = ll1 + ll2 + ll3 + ll4
    outer_sk = make_face(outer_lines)
    outer_body = extrude(outer_sk, height)

    main_body = outer_body - inner_body

    plane = Plane(main_body.faces()[1]) * Pos(
        -width / 2 + 1.5 * thickness, -height / 2, 0
    )

    pts = [
        (0, 0),  # 0
        (0, height / 3),  # 1
        (-width / 6, height * 2 / 3),  # 2
        (-width / 6, height),  # 3
        (-width / 6 + 1 * thickness, height),  # 4
        (-width / 6 + 1 * thickness, height * 2 / 3),  # 5
        (1 * thickness, height / 3),  # 6
        (1 * thickness, 0),  # 7
        (0, 0),  # 0
    ]

    slot_lines = Polyline(pts)

    slot_sk = plane * make_face(slot_lines)
    main_body -= extrude(slot_sk, -shell_thickness)

    main_body = fillet(main_body.edges().filter_by(Axis.Y)[-4:], radius=thickness)

    if n_shells >= 3:
        last_edges = main_body.edges().group_by(Axis.Y)[-1]
        main_body = chamfer(last_edges, length=shell_thickness / 2.5)
        # main_body = fillet(
        #     main_body.edges().filter_by(Axis.Z), radius=shell_thickness / 4
        # )


    part_file_name = f"strap_clip_{sid}.stl"
    # # Dictionary to store in-memory STL files
    # stl_files = {}
    # # Create an in-memory bytes buffer
    # stl_buffer = io.BytesIO()

    # # Create a temporary file
    # temp_file = tempfile.NamedTemporaryFile(delete=False)
    # temp_file.name = part_file_name
    # Create a temporary file with a specific prefix and suffix
    fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])

    # Close the file descriptor
    os.close(fd)

    # Export the object to STL format

    export_stl(main_body, temp_file_name)
    #
    # # Reset buffer position to the beginning
    # stl_buffer.seek(0)

    return temp_file_name



