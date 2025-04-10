# import build123d as bd
import tempfile
import os
from build123d import *
from math import pi, sin, cos, tan, asin, acos, atan, radians

dev_w = 80
dev_h = 140
dev_t = 12

slant = 20


## Gameboy:
# dev_w = 50
# dev_h = 100
# dev_t = 23

laptop_slot = True
laptop_thickness = 5.5

# def deg_to_rad(deg):
# return deg/180.0 * pi


def calc_points():
    pass


def derive_gadget_stand_vals(dev_w=80, dev_h=140, dev_t=12, slant=20, laptop_slot=False, laptop_thickness=5):
    ref_l = min(dev_w, dev_h)
    alpha_rad = radians(90 - slant)
    beta_rad = radians(slant)
    t_ref = min(2.0, dev_t / 6.0)

    l1 = t_ref / tan(beta_rad)
    l2 = t_ref / sin(beta_rad)
    l3 = dev_t * cos(beta_rad)
    l4 = dev_t * sin(beta_rad)
    xr = (l2 + dev_t + t_ref) / sin(alpha_rad)
    xrr = xr - l1 - l3
    yrr = t_ref + l4

    fl = xr * cos(alpha_rad) + 0.6 * dev_t

    l_slot_len = min(dev_t * 2.0, dev_w*0.85, dev_h *0.85)
    add_len = cos(alpha_rad) * max(dev_h,dev_w) * 0.5 + dev_t
    l_slot_add_length = 0
    if laptop_slot:
        l_slot_add_length = laptop_thickness / sin(alpha_rad) + l_slot_len * sin(beta_rad)
        l_slot_add_length *= 1.075 + (max(0,slant-20)/20) * 0.025
        #l_slot_add_length *= 1.2
        # print(l_slot_len, add_len, l_slot_add_length)
    xl = xr + max(add_len, l_slot_add_length)
    #xl = xr + cos(alpha_rad) * dev_h * 0.5 + dev_t

    return alpha_rad, beta_rad, xr, xrr, yrr, t_ref, fl, xl, l_slot_len



def build_dev(dev_w=80, dev_h=140, dev_t=12, slant=20):
    alpha_rad, beta_rad, xr, xrr, yrr, t_ref, fl, xl, l_slot_len = derive_gadget_stand_vals(
        dev_w, dev_h, dev_t, slant
    )
    x0 = xrr
    x1 = x0 + cos(alpha_rad) * dev_h
    x2 = x1 + sin(alpha_rad) * dev_t
    x3 = x0 + sin(alpha_rad) * dev_t

    y0 = yrr
    y1 = y0 + sin(alpha_rad) * dev_h
    y2 = y1 - cos(alpha_rad) * dev_t
    y3 = y0 - cos(alpha_rad) * dev_t

    pts = [(x0, y0), (x1, y1), (x2, y2), (x3, y3), (x0, y0)]

    dev_sk = make_face(Polyline(pts))
    dev = extrude(dev_sk, dev_w / 2.0)
    dev += mirror(dev, Plane.XY)

    c_l = min(dev_w, dev_h, dev_t) / 8.0
    dev = chamfer(dev.edges(), c_l)

    return dev


def build_stand(
    dev_w=80, dev_h=140, dev_t=12, slant=20, laptop_slot=True, laptop_thickness=5, sid=''
):
    # params_from_func = locals()
    msgs = []

    alpha_rad, beta_rad, xr, xrr, yrr, t_ref, fl, xl, l_slot_len = derive_gadget_stand_vals(
        dev_w, dev_h, dev_t, slant, laptop_slot, laptop_thickness
    )
    x0 = 0
    x1 = fl * cos(alpha_rad)
    x2 = x1 + t_ref * sin(alpha_rad)
    x3 = xrr
    x4 = x3 + dev_t * sin(alpha_rad)
    x5 = x4 + min(3.0 * dev_t,dev_w,dev_h) * cos(alpha_rad)
    x6 = xl
    x7 = xl

    y0 = 0
    y1 = fl * sin(alpha_rad)
    y2 = y1 - t_ref * cos(alpha_rad)
    y3 = yrr
    y4 = y3 - dev_t * cos(alpha_rad)
    y5 = y4 + min(3.0 * dev_t,dev_w,dev_h) * sin(alpha_rad)
    y6 = y5 * 0.65
    y7 = 0

    pts = [
        (x0, y0),
        (x1, y1),
        (x2, y2),
        (x3, y3),
        (x4, y4),
        (x5, y5),
        (x6, y6),
        (x7, y7),
        (x0, y0),
    ]

    stand_w = dev_w / 6.4

    stand_sk = make_face(Polyline(pts))
    stand = extrude(stand_sk, stand_w)

    edges = stand.edges().filter_by(Axis.Z)
    large_champfer_edges = []
    for se in [0, 5, 6, 7]:
        large_champfer_edges.append(edges[se])
    large_cmpf_len = min(stand_w / 2.0, t_ref * 2)
    stand = chamfer(large_champfer_edges, large_cmpf_len)

    edges = stand.edges().filter_by(Axis.Z)
    small_champfer_edges = []
    for se in [1, 3, 5, 7]:
        small_champfer_edges.append(edges[se])
    stand = chamfer(small_champfer_edges, t_ref / 4.0)

    butt_champfer_val = min(stand_w / 1.6, y6/3)
    stand = chamfer(stand.edges().filter_by(Axis.Y)[-1], butt_champfer_val)

    # laptop slot dims:
    sx0, sy0 = x4 + 2.0 * t_ref, 0
    sx1, sy1 = sx0 + l_slot_len * cos(alpha_rad), l_slot_len * sin(alpha_rad)
    sx2, sy2 = sx1 + laptop_thickness * sin(
        alpha_rad
    ), sy1 - laptop_thickness * cos(alpha_rad)
    sx3, sy3 = sx0 + laptop_thickness / sin(alpha_rad), 0

    if laptop_slot:
        if laptop_thickness >= dev_t * 2.5:
            msgs.append("Laptop thickness is a bit too much. t should not be much more than twice the thickness of the device, as it could bend the laptop monitor.")
        else:
            try:
                s_pts = [(sx0, sy0), (sx1, sy1), (sx2, sy2), (sx3, sy3), (sx0, sy0)]

                laptop_slot_sk = make_face(Polyline(s_pts))
                laptop_slot = extrude(laptop_slot_sk, stand_w)
                snapshot = stand.edges()
                stand -= laptop_slot
                new_edges = stand.edges() - snapshot
                fillet_rad = min(laptop_thickness / 4.0, dev_t / 4.0, sy2/6.0)
                try:
                    stand = fillet(new_edges.group_by(Axis.Z)[-2], fillet_rad)
                    # stand = chamfer(new_edges.group_by(Axis.Y)[-1], t_ref/4.0)
                except:
                    try:
                        stand = fillet(new_edges.group_by(Axis.Z)[-2], fillet_rad/4)
                    except Exception as e:
                        msgs.append(f"""Was not able to create a fillet on laptop slot opening.
                            Maybe the laptop slot is much larger then the device thickness?
                            {e}""")
            except Exception as e:
                msgs.append(f"""Was not able to create laptop slot opening.
                            Maybe the laptop slot is much larger then the device thickness?
                            {e}""")

    outer_chmf_len = min(t_ref / 4.0, laptop_thickness / 6.0, dev_t / 4.0, abs(sy2/6.0), y4/6.0, stand_w/10.0)
    try:
        stand = chamfer(stand.edges().group_by(Axis.Z)[-1], outer_chmf_len)
    except Exception as e:
        msgs.append(f"Something went abot wrong with creating the outher champfer:\n{e}")

    # The elephant gets an eye:
    eye = Pos((x5 + sx1) / 2 + t_ref / 1.75, (y5 + sy1) / 2, stand_w) * Sphere(radius=t_ref / 1.75)
    stand -= eye

    stand += mirror(stand, Plane.XY)

    return stand, msgs


def create_gadget_stand_V01(dev_w=80, dev_h=140, dev_t=12, slant=20, laptop_slot=True, laptop_thickness=5):

    params = locals()
    params_string = ""
    for k,v in params.items():
        params_string += f"-{k}-{v}".replace('.','d')
    part_file_name = f"gadget_stand_v01{params_string}.stl"
    temp_dir = tempfile.gettempdir()
    custom_temp_path = os.path.join(temp_dir, part_file_name)
    msgs_file = custom_temp_path.replace('.stl','.msg')
    messages = []
    if not os.path.isfile(custom_temp_path):
        pyvista_part, messages = build_stand(dev_w, dev_h, dev_t, slant, laptop_slot, laptop_thickness)
        export_stl(pyvista_part, custom_temp_path)

        with open(msgs_file, 'w') as msg_file:
            msg_file.writelines([m+'\n' for m in messages])

    else:
        with open(msgs_file, 'r') as msg_file:
            messages = msg_file.readlines()

    return custom_temp_path, messages


def create_gadget_dummy_V01(dev_w=80, dev_h=140, dev_t=12, slant=20):

    params = locals()
    params_string = ""
    for k,v in params.items():
        params_string += f"-{k}-{v}".replace('.','d')
    part_file_name = f"gadget_dummy_v01{params_string}.stl"
    temp_dir = tempfile.gettempdir()
    custom_temp_path = os.path.join(temp_dir, part_file_name)

    if not os.path.isfile(custom_temp_path):
        pyvista_part = build_dev(dev_w, dev_h, dev_t, slant)
        export_stl(pyvista_part, custom_temp_path)

    return custom_temp_path


# device = build_dev(dev_w, dev_h, dev_t, slant)
# stand = build_stand(dev_w, dev_h, dev_t, slant, laptop_slot, laptop_thickness)
#
#
# show_object(device, options={"color": (200, 200, 200)})
# show_object(stand)
