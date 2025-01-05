# import build123d as bd
from build123d import *

h_width = 10
h_thickness = 6
h_height = 10

b_width = 80
b_thickness = 8
b_height = 10

screw_dia = 3.2
screw_dpt = h_height + b_height - 2
screw_distance = 64

handle_champfer_l = h_height / 4
fillet_rad = (h_thickness-b_thickness)/6



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

#base_plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1]) * Pos(
#        -7 / 2 + 1.5 * 4, -4 / 2, 0
#    )

base_plane_screw_hole = Plane(base_handle.faces().sort_by(Axis.Z)[0])
base_handle -= (
    base_plane_screw_hole
    * Pos(screw_distance/2, 0, 0)
    * CounterSinkHole(radius=screw_dia / 2, counter_sink_radius=(screw_dia / 2)*1.25, depth=screw_dpt)
)
base_handle -= (
    base_plane_screw_hole
    * Pos(-screw_distance/2, 0, 0)
    * CounterSinkHole(radius=screw_dia / 2, counter_sink_radius=(screw_dia / 2)*1.25, depth=screw_dpt)
)

try:
    base_handle = fillet(base_handle.edges().filter_by(Axis.X)[7], radius=fillet_rad)
except:
    print("was not able to create fillet")

# Add text
#plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1])* Pos(0, 6, 0)
#ex34_sk2 = plane * Text("MegaShaper", font_size=15, align=(Align.CENTER, Align.MAX))
#base_handle -= extrude(ex34_sk2, amount=-1)

#screw_hole = Cylinder(screw_dia / 2, height=screw_dpt) * Pos(2,4,5)
export_stl(base_handle, "handle_test_02.stl")
show_object(base_handle)
#show_object(h_body)
#show_object(screw_hole)



