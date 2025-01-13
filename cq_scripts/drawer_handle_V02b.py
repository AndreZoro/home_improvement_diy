# import build123d as bd
from build123d import *
from math import pi, tan

h_width = 80
h_thickness = 6
h_height = 60
h_rad = 40
b_thickness = 10
screw_distance = 64
screw_dia = "m4"
slant_ang = 30
front_text = "Töpfe"
sid = "test"


def get_handle_dims(h_height, h_width, slant_ang):
    h_delta_x = h_height * tan(slant_ang * pi / 180)
    print(f"Height: {h_height}, angle: {slant_ang}, deltaX: {h_delta_x}")
    mid_width = h_width

    pts = [
        ((-mid_width + h_delta_x) / 2.0, h_height / 2.0),
        ((mid_width + h_delta_x) / 2.0, h_height / 2.0),
        ((mid_width - h_delta_x) / 2.0, -h_height / 2.0),
        ((-mid_width - h_delta_x) / 2.0, -h_height / 2.0),
        ((-mid_width + h_delta_x) / 2.0, h_height / 2.0),
    ]

    return h_delta_x, mid_width, pts


def create_build123d_handle_v02(
    h_width=100,
    h_thickness=4,
    h_height=25,
    h_rad=30,
    b_thickness=8,
    screw_distance=64,
    screw_dia="m2",
    slant_ang=-25,
    front_text="",
    sid="",
):

    # Constants
    screw_dia_shrinkage = 0.9

    # Derived Vals
    msgs = []
    screw_dia = float(screw_dia.replace("m", ""))
    if screw_distance < 6 * screw_dia:
        screw_distance = 6 * screw_dia
        msgs.append(
            "Increased screw distance, as it was to low for the selected screw type"
        )
    screw_dia_shrunk = screw_dia * screw_dia_shrinkage

    b_width = screw_distance + screw_dia * 4
    b_height = screw_dia * 3
    # print(f"Base width: {b_width}, Base height: {b_height}")

    screw_dpt = h_thickness + b_thickness - 2

    if screw_dpt < 2 * screw_dia:
        msgs.append(
            "The maximum screw depth is a bit to short. Try increasing base thickness."
        )

    handle_champfer_l = min(h_thickness / 4, b_thickness / 4)

    # derived for handle
    h_delta_x, mid_width, h_pts = get_handle_dims(h_height, h_width, slant_ang)

    print(f"bwidth: {b_width} \t h width: {h_width}")
    print(f"{mid_width + 4*handle_champfer_l + 2*screw_dia} \t {b_width * 1.25}")
    if mid_width < ((b_width + 4 * handle_champfer_l + 2 * screw_dia) * 1.2):
        # TODO: This recaclulation is a bit wrong
        h_width = (
            b_width * 1.2 + 6 * handle_champfer_l + b_height * abs(slant_ang) / 45 * 0.1
        )
        handle_champfer_l *= 0.5
        print(f"H Widht increased to: {h_width}")
        msgs.append(
            f"Handle width was too small for the screw distance. Handle width gets automatically increased to {h_width}mm."
        )
        h_delta_x, mid_width, h_pts = get_handle_dims(h_height, h_width, slant_ang)

    if h_height < b_height * 1.2:
        h_height = b_height * 1.25 + 6 * handle_champfer_l
        handle_champfer_l *= 0.5
        print(
            f"Handle height was too small for the selected screw type. Handle height gets automatically increased to {h_width}mm."
        )
        h_delta_x, mid_width, h_pts = get_handle_dims(h_height, h_width, slant_ang)

    print(f"\nValues now at: {h_width} - {h_thickness} - {h_height}")
    # Add width params as well
    fillet_rad = (
        min(abs(h_height - b_height), abs(b_width - b_height), b_height * 2) / 8
    )

    # corner rad
    h_c_rad = max((h_height / 2.0) * (h_rad / 100.0) * 0.98, 0.1)
    if h_c_rad <= 2 * handle_champfer_l:
        h_c_rad = 2.0 * handle_champfer_l

    font_size = int(h_height * 0.75)
    font_pos = int(font_size / 4)
    font_deepness = min(1, h_thickness / 4)

    # Geo generation
    # base lines
    x_corner = (b_width / 2) - (b_height / 2)
    y_corner = b_height / 2
    l1 = Line((-x_corner, y_corner), (x_corner, y_corner))
    l2 = ThreePointArc(
        (x_corner, y_corner),
        (x_corner + b_height / 2, 0),
        (x_corner, -y_corner),
    )
    l3 = Line((x_corner, -y_corner), (-x_corner, -y_corner))
    l4 = ThreePointArc(
        (-x_corner, -y_corner),
        (-x_corner - b_height / 2, 0),
        (-x_corner, y_corner),
    )

    base_lines = l1 + l2 + l3 + l4
    base_sk = make_face(base_lines)
    base_body = extrude(base_sk, -b_thickness)

    # handle lines

    h_lines = Polyline(h_pts)
    h_sk = make_face(h_lines)
    h_body = extrude(h_sk, h_thickness)
    try:
        h_body = fillet(h_body.edges().filter_by(Axis.Z), radius=h_c_rad)
    except:
        try:
            h_body = fillet(h_body.edges().filter_by(Axis.Z), radius=h_c_rad / 2)
            msgs.append(
                "Had trouble creating a radius in the front handle face edge corners. I created a smaller one. Maybe your slant angle and handle hight are a bit extreme."
            )
        except:
            msgs.append(
                "Had trouble creating a radius in the front handle face edge corners. I was not able to create the rounded corners. Maybe your slant angle and handle hight are a bit extreme."
            )

    try:
        h_body = chamfer(h_body.edges(), length=handle_champfer_l)
    except:
        try:
            h_body = chamfer(h_body.edges(), length=handle_champfer_l * 0.25)
            msgs.append(
                "Had to reduce champfer size for front handle face. No idea why. Some dimension is a bit too tclose to another one."
            )
        except:
            msgs.append(
                "Was not able to create a nice champfer on the front handle face. I do not know why. Check all dimensions, something, somewhere is too close to something else."
            )

    base_handle = h_body + base_body

    # base_plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1]) * Pos(
    #        -7 / 2 + 1.5 * 4, -4 / 2, 0
    #    )

    base_plane_screw_hole = Plane(base_handle.faces().sort_by(Axis.Z)[0])
    base_handle -= (
        base_plane_screw_hole
        * Pos(screw_distance / 2, 0, 0)
        * CounterSinkHole(
            radius=screw_dia_shrunk / 2,
            counter_sink_radius=(screw_dia_shrunk / 2) * 1.25,
            depth=screw_dpt,
        )
    )
    base_handle -= (
        base_plane_screw_hole
        * Pos(-screw_distance / 2, 0, 0)
        * CounterSinkHole(
            radius=screw_dia_shrunk / 2,
            counter_sink_radius=(screw_dia_shrunk / 2) * 1.25,
            depth=screw_dpt,
        )
    )

    try:
        base_handle = fillet(
            base_handle.edges().filter_by(Axis.X)[6], radius=fillet_rad
        )
    except:
        msgs.append(
            "Was not able to create fillet between base and front face. Try increasing height or width of front part."
        )
        # breakpoint()
        # max_fillet = base_handle.max_fillet(base_handle.edges().filter_by(Axis.X), tolerance=fillet_rad/2, max_iterations=40)
        # max_fillet = max_fillet * 0.8
        # try:
        #     base_handle = fillet(base_handle.edges().filter_by(Axis.X)[6], radius=max_fillet)
        # except:
        #     msgs.append("Was not able to create fillet between base and front face. Try increasing height or width of front part.")

    # Add text
    if front_text != "":
        plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1]) * Pos(0, font_pos, 0)
        ex34_sk2 = plane * Text(
            front_text, font_size=25, align=(Align.CENTER, Align.MAX)
        )
        base_handle -= extrude(ex34_sk2, amount=-font_deepness)

    part_file_name = f"drawer_handle_{sid}.stl"
    # fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])
    # os.close(fd)
    # export_stl(base_handle, temp_file_name)

    if len(msgs) == 0:
        msgs.append("Part generated successfully.")

    return base_handle  # , msgs, part_file_name


# geo_part = create_build123d_handle_v02(h_width,h_thickness,h_height,h_rad,b_thickness,screw_distance,screw_dia,slant_ang,front_text,sid)
geo_part = create_build123d_handle_v02(
    h_width,
    h_thickness,
    h_height,
    h_rad,
    b_thickness,
    screw_distance,
    screw_dia,
    slant_ang,
    front_text,
    sid,
)


show_object(geo_part)
export_stl(geo_part, "drawer_handle_V02.stl")
