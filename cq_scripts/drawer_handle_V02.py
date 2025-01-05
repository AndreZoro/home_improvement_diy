from math import pi, tan
# import build123d as bd
from build123d import *


def get_handle_dims(h_height, h_width, slant_ang):
    h_delta_x = h_height * tan(slant_ang * pi / 180)
    mid_width = h_width - h_delta_x
    
    pts = [
        ((-mid_width + h_delta_x) / 2.0, h_height / 2.0),
        ((mid_width + h_delta_x) / 2.0, h_height / 2.0),
        ((mid_width - h_delta_x) / 2.0, -h_height / 2.0),
        ((-mid_width -
          h_delta_x) / 2.0, -h_height / 2.0),
        ((-mid_width + h_delta_x) / 2.0, h_height / 2.0),
    ]
    
    return h_delta_x, mid_width, pts
    


# Input Vars
h_width = 120
h_thickness = 4
h_height = 30
h_rad = 30

b_thickness = 8

screw_distance = 64
screw_dia = 'm4'

slant_ang = -25

front_text = 'MegaShaper'

# Constants
screw_dia_shrinkage = 0.9


# Derived Vals
msgs = []
screw_dia = float(screw_dia.replace('m',''))
screw_dia_shrunk = screw_dia * screw_dia_shrinkage

b_width = screw_distance + screw_dia * 4
b_height = screw_dia * 3
print(f"Base width: {b_width}, Base height: {b_height}")

screw_dpt = h_thickness + b_thickness - 2

if screw_dpt < 2 * screw_dia:
    msgs.append("The maximum screw depth is a bit to short. Try increasing base thickness.")


handle_champfer_l = h_thickness / 4

# Add width params as well
fillet_rad = min((h_height-b_height),(200)) / 40


# derived for handle
h_delta_x, mid_width, h_pts = get_handle_dims(h_height, h_width, slant_ang)

if mid_width * 1.1 < b_width:
    # TODO: This recaclulation is a bit wrong
    h_width = b_width * 1.2
    msgs.append(f"Handle with was too small for the screw distance. Handle width gets automatically increased to {h_width}mm.")
    h_delta_x, mid_width, h_pts = get_handle_dims(h_height, h_width, slant_ang)

# corner rad
h_c_rad = h_height / 2 * h_rad / 100 - h_height / 100

font_size = int(h_height * 0.75)
font_pos = int(font_size/4)

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
h_body = fillet(h_body.edges().filter_by(Axis.Z), radius=h_c_rad)
h_body = chamfer(h_body.edges(), length=handle_champfer_l)

base_handle = h_body + base_body

#base_plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1]) * Pos(
#        -7 / 2 + 1.5 * 4, -4 / 2, 0
#    )

base_plane_screw_hole = Plane(base_handle.faces().sort_by(Axis.Z)[0])
base_handle -= (
    base_plane_screw_hole
    * Pos(screw_distance/2, 0, 0)
    * CounterSinkHole(radius=screw_dia_shrunk / 2, counter_sink_radius=(screw_dia_shrunk / 2)*1.25, depth=screw_dpt)
)
base_handle -= (
    base_plane_screw_hole
    * Pos(-screw_distance/2, 0, 0)
    * CounterSinkHole(radius=screw_dia_shrunk / 2, counter_sink_radius=(screw_dia_shrunk / 2)*1.25, depth=screw_dpt)
)


#base_handle = fillet(base_handle.edges().filter_by(Axis.X)[7], radius=fillet_rad)


# Add text
if front_text != "":
    plane = Plane(base_handle.faces().sort_by(Axis.Z)[-1])* Pos(0, font_pos, 0)
    ex34_sk2 = plane * Text(front_text, font_size=15, align=(Align.CENTER, Align.MAX))
    base_handle -= extrude(ex34_sk2, amount=-1)



#screw_hole = Cylinder(screw_dia / 2, height=screw_dpt) * Pos(2,4,5)
export_stl(base_handle, "handle_test_02.stl")
show_object(base_handle)
#show_object(h_body)
#show_object(screw_hole)



